import redis
import json
from datetime import datetime, timedelta
import time

from core.apis.mailgun import MailGunConfig
from core.repositories.scheduled_job_repository import get_repository as get_job_repository
from server.services.task_runner.jobs.sync_accounts import SyncAccounts

from server.config import config as server_config
from server.services.api import load_config
app_config = load_config()

sql_config = app_config['db']
mailgun_config = MailGunConfig(api_key=server_config['mailgun']['api_key'],
                               domain=server_config['mailgun']['domain'])

WORKER_QUEUE = "mp:worker"


class Runner:

    thread = None
    running = False
    timer_start = None

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        self.job_repo = get_job_repository(mysql_config=sql_config, mailgun_config=mailgun_config)
        self.pubsub.subscribe(**{WORKER_QUEUE: self.__fetch_jobs})
        self.jobs = self.job_repo.get_scheduled_jobs()
        print(" * found {0} scheduled jobs".format(len(self.jobs)), flush=True)

    def run(self):
        self.running = True
        self.thread = self.pubsub.run_in_thread(sleep_time=0.1)
        while self.running:
            # run every minute, regardless of how long the last run took
            self.timer_start = datetime.utcnow()
            self.__run_scheduler()
            sleep_time = datetime.utcnow() - self.timer_start
            time_delta = 60 - sleep_time.seconds
            time.sleep(time_delta)
        self.thread.join()

    def stop(self):
        self.running = False

    def __fetch_jobs(self, message):
        print(" * found message on worker queue: {0}".format(message), flush=True)
        json_data = json.loads(message['data'])
        job = json_data['job']
        if job is not None:
            # todo - figure out some way to dynamically dispatch this
            if job == 'sync_accounts':
                print(" * syncing accounts for plaid access item", flush=True)
                job = SyncAccounts(json_data)
                job.run()

    def __run_scheduler(self):
        # doesn't really 'run' a scheduler, but it's polled every second while the server is up
        # so we can pull the data jobs in the db and check them against the time and run them
        # if it applies
        ran_jobs_count = 0
        for job in self.jobs:
            job_ran = False
            timedelta_val = None

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
                print(" * scheduling {0} job {1}, last run: {2}".format(job.frequency_type, job.job_name, last_run_iso),flush=True)

                self.redis.publish(WORKER_QUEUE, json.dumps({
                   'job': job.job_name,
                   'data': job.json_args
                }))
                job_ran = True

            if job_ran:
                self.job_repo.update_last_run(job)
                ran_jobs_count += 1

        if ran_jobs_count > 0:
            print(" * task runner scheduled {0} jobs".format(ran_jobs_count),flush=True)
