from datetime import datetime
import json

import redis
from rq import Queue
from rq_scheduler import Scheduler

from core.apis.mailgun import MailGun
from core.stores.mysql import MySql
from core.models.scheduler.scheduled_job import ScheduledJob
from core.models.scheduler.job_result import JobResult
from core.lib.types import ScheduledJobList
from core.lib.constants import WORKER_QUEUE
from config import redis_config, mailgun_config, mysql_config

# import all the actions so that consumers of the repo can access everything
from core.lib.actions.scheduled_job.requests import *


class ScheduledJobRepository:

    db = MySql(mysql_config)
    redis = redis.Redis(host=redis_config['host'], port=redis_config['port'], db=0)
    mailgun_client = MailGun(mailgun_config)
    queues = []

    def get_scheduled_jobs(self) -> ScheduledJobList:
        """
        Gets all ScheduledJobs
        """
        r = self.db.with_session(lambda session: session.query(ScheduledJob).all())
        return r

    def get_scheduled_job_by_id(self, id: int):
        """
        Gets a ScheduledJob by it's primary key
        """
        r = self.db.with_session(lambda session: session.query(ScheduledJob)
                                 .where(ScheduledJob.id == id)).first()
        return r

    def create_instant_job(self, request: CreateInstantJobRequest):
        """
        Pushes a message into Redis to perform the requested job ASAP
        """
        q = self.get_or_create_queue(WORKER_QUEUE)
        job = q.enqueue(request.job_name, request.args)
        return job

    def create_scheduled_job(self, request: CreateScheduledJobRequest):
        """
        Creates a record in the DB to schedule a job in the worker
        """
        job = ScheduledJob()
        job.job_name = request.job_name
        job.cron = request.cron
        job.json_args = request.json_args
        job.last_run = None
        job.queue = WORKER_QUEUE
        job.timestamp = datetime.utcnow()

        def save_job(session):
            session.add(job)
            session.commit()

        self.db.with_session(save_job)

        self.ensure_scheduled(WORKER_QUEUE, job)

        return job

    def update_scheduled_job(self, job):
        self.unschedule_job(job.queue, job)

        def save_job(session):
            session.add(job)
            session.commit()
        self.db.with_session(save_job)

        self.ensure_scheduled(job.queue, job)

    def delete_scheduled_job(self, job):
        self.unschedule_job(job.queue, job)

        def delete_job(session):
            session.remove(job)
            session.commit()

        self.db.with_session(delete_job)

    def enqueue_scheduled_job(self, job):
        q = self.get_or_create_queue(job.queue)
        q.enqueue(job.job_name, job.json_args)

    def schedule_persistent_jobs(self):
        jobs = self.get_scheduled_jobs()
        for job in jobs:
            self.ensure_scheduled(job.queue, job)

    def update_last_run(self, job: ScheduledJob) -> ScheduledJob:
        """
        Update the last run time of a ScheduledJob
        """
        job.last_run = datetime.utcnow()
        job.timestamp = datetime.utcnow()

        def save_job(session):
            session.add(job)
            session.commit()

        self.db.with_session(save_job)

        return job

    def ensure_scheduled(self, queue: str, job):
        scheduler = self.get_scheduler(queue)
        jobs = scheduler.get_jobs()
        if queue not in [j.meta['id'] for j in jobs]:
            scheduler.cron(job.cron, job.job_name, args=job.json_args, meta={
                'id': job.id
            })

    def unschedule_job(self, queue: str, job):
        scheduler = self.get_scheduler(queue)
        jobs = scheduler.get_jobs()
        scheduler_job = [j for j in jobs if j.func == job.job_name][0]
        if scheduler_job:
            scheduler.cancel(job)

    def get_or_create_queue(self, name: str):
        queue_names = [q.name for q in self.queues]
        if name in queue_names:
            return [q for q in self.queues if q.name == name][0]
        else:
            q = Queue(name, connection=self.redis, on_success=self.store_success, on_failure=self.store_failure)
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

        def save_job_result(session):
            session.add(result)
            session.commit()

        self.db.with_session(save_job_result)

    def store_failure(self, job, connection, type, value, traceback):
        result = JobResult()
        result.job_id = job.id
        result.success = False
        result.log = traceback
        result.queue = job.queue
        result.timestamp = datetime.utcnow()

        def save_job_result(session):
            session.add(result)
            session.commit()

        self.db.with_session(save_job_result)


