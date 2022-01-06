from datetime import datetime
import json

import redis
from rq import Queue
from rq_scheduler import Scheduler

from core.apis.mailgun import MailGun
from core.stores.database import Database
from core.models import ScheduledJob, JobResult
from core.schemas import CreateScheduledJobSchema, CreateInstantJobSchema
from core.lib.constants import WORKER_QUEUE
from core.repositories.repository_response import RepositoryResponse
from config import redis_config, mailgun_config


class ScheduledJobRepository:

    db = Database()
    redis = redis.Redis(
        host=redis_config['host'], port=redis_config['port'], db=0)
    mailgun_client = MailGun(mailgun_config)
    queues = []

    def get_scheduled_jobs(self) -> RepositoryResponse:
        """
        Gets all ScheduledJobs
        """
        with self.db.get_session() as session:
            jobs = session.query(ScheduledJob).all()

        return RepositoryResponse(
            success=jobs is not None,
            data=jobs,
            message=f"No scheduled jobs found" if jobs is None else None
        )

    def get_scheduled_job_by_id(self, id: int) -> RepositoryResponse:
        """
        Gets a ScheduledJob by it's primary key
        """
        with self.db.get_session() as session:
            job = session.query(ScheduledJob).where(
                ScheduledJob.id == id).first()

        return RepositoryResponse(
            success=job is not None,
            data=job,
            message=f"No ScheduledJob found with ID {id}" if job is None else None
        )

    def create_instant_job(self, request: CreateInstantJobSchema) -> RepositoryResponse:
        """
        Pushes a message into Redis to perform the requested job ASAP
        """
        q = self.get_or_create_queue(WORKER_QUEUE)
        job = q.enqueue(request['job_name'], request['json_args'])

        return RepositoryResponse(
            success=job is not None,
            data=job,
            message=f"Error enqueuing job" if job is None else None
        )

    def create_scheduled_job(self, request: CreateScheduledJobSchema) -> RepositoryResponse:
        """
        Creates a record in the DB to schedule a job in the worker
        """
        job = ScheduledJob()
        job.job_name = request['job_name']
        job.cron = request['cron']
        job.json_args = request['json_args']
        job.last_run = None
        job.queue = WORKER_QUEUE
        job.timestamp = datetime.utcnow()

        with self.db.get_session() as session:
            session.add(job)
            session.commit()

        self.ensure_scheduled(WORKER_QUEUE, job)

        return RepositoryResponse(
            success=job is not None,
            data=job,
            message=f"Error creating job" if job is None else None
        )

    def update_scheduled_job(self, job) -> RepositoryResponse:
        self.unschedule_job(job.queue, job)

        with self.db.get_session() as session:
            session.add(job)
            session.commit()

        return self.ensure_scheduled(job.queue, job)

    def delete_scheduled_job(self, job) -> RepositoryResponse:
        self.unschedule_job(job.queue, job)

        with self.db.get_session() as session:
            session.delete(job)
            session.commit()

        return RepositoryResponse(
            success=True
        )

    def enqueue_scheduled_job(self, job) -> RepositoryResponse:
        q = self.get_or_create_queue(job.queue)
        q.enqueue(job.job_name, job.json_args)

        return RepositoryResponse(
            success=True
        )

    def schedule_persistent_jobs(self) -> RepositoryResponse:
        result = self.get_scheduled_jobs()
        if not result.success:
            return result
        for job in result.data:
            self.ensure_scheduled(job.queue, job)

        return RepositoryResponse(
            success=True
        )

    def update_last_run(self, job: ScheduledJob) -> RepositoryResponse:
        """
        Update the last run time of a ScheduledJob
        """
        job.last_run = datetime.utcnow()
        job.timestamp = datetime.utcnow()

        with self.db.get_session() as session:
            session.add(job)
            session.commit()

        return RepositoryResponse(
            success=job is not None,
            data=job,
            message=f"Error creating scheduled job" if job is None else None
        )

    def ensure_scheduled(self, queue: str, job) -> RepositoryResponse:
        scheduler = self.get_scheduler(queue)
        jobs = scheduler.get_jobs()
        if queue not in [j.meta['id'] for j in jobs]:
            scheduler.cron(job.cron, job.job_name, args=job.json_args, meta={
                'id': job.id
            })

        return RepositoryResponse(
            success=True
        )

    def unschedule_job(self, queue: str, job) -> RepositoryResponse:
        scheduler = self.get_scheduler(queue)
        jobs = scheduler.get_jobs()
        scheduler_job = [j for j in jobs if j.func == job.job_name][0]
        if scheduler_job:
            scheduler.cancel(job)

        return RepositoryResponse(
            success=True
        )

    def get_or_create_queue(self, name: str):
        queue_names = [q.name for q in self.queues]
        if name in queue_names:
            return [q for q in self.queues if q.name == name][0]
        else:
            q = Queue(name, connection=self.redis,
                      on_success=self.store_success, on_failure=self.store_failure)
            self.queues.append({
                'name': name,
                'queue': q
            })
            return q

    def get_scheduler(self, name: str):
        q = self.get_or_create_queue(name)
        return Scheduler(queue=q)

    def store_success(self, job, connection, result, *args, **kwargs):
        result = JobResult()
        result.job_id = job.id
        result.success = True
        result.log = result
        result.queue = job.queue
        result.timestamp = datetime.utcnow()

        with self.db.get_session() as session:
            session.add(result)
            session.commit()

    def store_failure(self, job, connection, type, value, traceback):
        result = JobResult()
        result.job_id = job.id
        result.success = False
        result.log = traceback
        result.queue = job.queue
        result.timestamp = datetime.utcnow()

        with self.db.get_session() as session:
            session.add(result)
            session.commit()
