from datetime import datetime
import json

import redis

from core.apis.mailgun import MailGun
from core.stores.mysql import MySql
from core.models.scheduled_job import ScheduledJob
from core.lib.types import ScheduledJobList
from core.lib.constants import WORKER_QUEUE
from config import redis_config, mailgun_config, mysql_config

# import all the facets so that consumers of the repo can access everything
from .facets.scheduled_job.requests import *


class ScheduledJobRepository:

    def __init__(self):
        self.mailgun_client = MailGun(mailgun_config)
        db = MySql(mysql_config)
        self.db = db.get_session()
        self.redis = redis.Redis(host=redis_config['host'], port=redis_config['port'], db=0)

    def create_instant_job(self, request: CreateInstantJobRequest):
        """
        Pushes a message into Redis to perform the requested job ASAP
        """
        self.redis.publish(WORKER_QUEUE, json.dumps({
            'job': request.job_name,
            'args': request.args
        }))

    def create_scheduled_job(self, request: CreateScheduledJobRequest):
        """
        Creates a record in the DB to schedule a job in the worker
        """
        job = ScheduledJob()
        job.job_name = request.job_name
        job.frequency_type = request.frequency_type
        job.frequency_value = request.frequency_value
        job.json_args = request.json_args
        job.last_run = None
        job.timestamp = datetime.utcnow()

        self.db.add(job)
        self.db.commit()

        return job

    def get_scheduled_jobs(self) -> ScheduledJobList:
        """
        Gets all ScheduledJobs
        """
        r = self.db.query(ScheduledJob).all()
        return r

    def update_last_run(self, job: ScheduledJob) -> ScheduledJob:
        """
        Update the last run time of a ScheduledJob
        """
        job.last_run = datetime.utcnow()
        job.timestamp = datetime.utcnow()

        self.db.add(job)
        self.db.commit()

        return job
