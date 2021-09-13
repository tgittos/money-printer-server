from datetime import datetime

from core.apis.mailgun import MailGun, MailGunConfig
from core.stores.mysql import MySql
from core.models.scheduled_job import ScheduledJob


def get_repository(mailgun_config, mysql_config):
    repo = ScheduledJobRepository(ScheduledJobRepositoryConfig(
        mailgun_config=mailgun_config,
        mysql_config=mysql_config
    ))
    return repo


class ScheduledJobRepositoryConfig:
    def __init__(self, mailgun_config, mysql_config):
        self.mailgun_config = mailgun_config
        self.mysql_config = mysql_config


class CreateScheduledJobRequest:
    def __init__(self, job_name, frequency_type, frequency_value):
        self.job_name = job_name
        self.frequency_type = frequency_type
        self.frequency_value = frequency_value


class ScheduledJobRepository:

    def __init__(self, config):
        self.mailgun_client = MailGun(config.mailgun_config)
        db = MySql(config.mysql_config)
        self.db = db.get_session()

    def create_scheduled_job(self, request):
        job = ScheduledJob()
        job.job_name = request.job_name
        job.frequency_type = request.frequency_type
        job.frequency_value = request.frequency_value
        job.timestamp = datetime.utcnow()

        self.db.add(job)
        self.db.commit()

        return job

    def get_scheduled_jobs(self):
        r = self.db.query(ScheduledJob).all()
        return r

    def update_last_run(self, job):
        job.last_run = datetime.utcnow()

        self.db.add(job)
        self.db.commit()

        return job
