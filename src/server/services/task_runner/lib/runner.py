import redis
import json
from datetime import datetime, timedelta, timezone
import time
from threading import Thread

from core.repositories.scheduled_job_repository import get_repository as get_job_repository
from core.lib.logger import get_logger
from config import redis_config, mysql_config, mailgun_config

WORKER_QUEUE = "mp:worker"


class Runner(Thread):

    running = False
    timer_start = None
    on_error = None
    exception_count = 0

    def __init__(self):
        super(Runner, self).__init__()
        self.logger = get_logger(__name__)
        self.redis = redis.Redis(host=redis_config.host, port=redis_config.port, db=0)
        self.job_repo = get_job_repository(mysql_config=mysql_config, mailgun_config=mailgun_config)
        self.jobs = self.job_repo.get_scheduled_jobs()
        self.logger.info("found {0} scheduled jobs".format(len(self.jobs)))

    def start(self) -> None:
        self.logger.debug("scheduled job runner thread starting")
        self.running = True
        super(Runner, self).start()

    def stop(self) -> None:
        self.logger.debug("shutting job runner thread down")
        self.running = False
        super(Runner, self).join()

    def run(self):
        while self.running:
            try:
                # run every minute, regardless of how long the last run took
                self.timer_start = datetime.utcnow()
                self.__run_scheduler()
                self.exception_count = 0
                sleep_time = datetime.utcnow() - self.timer_start
                time_delta = 60 - sleep_time.seconds
                time.sleep(time_delta)
            except Exception as ex:
                self.exception_count += 1
                if self.exception_count == 10:
                    # 10 exceptions since we had a clean run? either the runner or a job entry is borked
                    self.logger.error("too many exceptions in a row, shutting the runner down")
                    self.running = False
                if self.on_error is not None:
                    self.on_error(ex)
                else:
                    self.logger.exception(" * caught exception but no handler defined, swallowing: {0}".format(ex))

    def __run_scheduler(self):
        # doesn't really 'run' a scheduler, but it's polled every second while the server is up
        # so we can pull the data jobs in the db and check them against the time and run them
        # if it applies
        ran_jobs_count = 0
        for job in self.jobs:
            job_ran = False
            timedelta_val = None

            if job.frequency_type == "scheduled":
                time_val = datetime.strptime(job.frequency_value, "%H:%M")
                next_run = datetime.now(tz=timezone.utc)
                last_run = None
                if job.last_run:
                    last_run = job.last_run.astimezone(tz=timezone.utc)
                    next_run = datetime.now(tz=timezone.utc).replace(hour=time_val.hour, minute=time_val.minute)
                if last_run is None or last_run < next_run <= datetime.now(tz=timezone.utc):
                    last_run_iso = "never"
                    if last_run is not None:
                        last_run_iso = last_run.isoformat()
                    self.logger.info(" * scheduling {0} job {1}, last run: {2}".format(job.frequency_type, job.job_name,
                                                                                       last_run_iso))
                    self.redis.publish(WORKER_QUEUE, json.dumps({
                        'job': job.job_name,
                        'args': job.json_args
                    }))
                    job_ran = True
            else:
                if job.frequency_type == "hourly":
                    timedelta_val = timedelta(hours=int(job.frequency_value))
                if job.frequency_type == "daily":
                    timedelta_val = timedelta(days=int(job.frequency_value))
                if job.frequency_type == "weekly":
                    timedelta_val = timedelta(weeks=int(job.frequency_value))

                if job.last_run is None or timedelta_val is not None and job.last_run + timedelta_val <= datetime.utcnow():
                    # run the job, then update it's status
                    last_run_iso = "never"
                    if job.last_run is not None:
                        last_run_iso = job.last_run.isoformat()
                    self.logger.info(" * scheduling {0} job {1}, last run: {2}".format(job.frequency_type, job.job_name,
                                                                                       last_run_iso))
                    self.redis.publish(WORKER_QUEUE, json.dumps({
                       'job': job.job_name,
                       'data': job.json_args
                    }))
                    job_ran = True

            if job_ran:
                self.job_repo.update_last_run(job)
                ran_jobs_count += 1

        if ran_jobs_count > 0:
            self.logger.info(" * task runner scheduled {0} jobs".format(ran_jobs_count))
