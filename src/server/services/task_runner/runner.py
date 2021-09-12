import redis

from server.services.task_runner.jobs.sync_accounts import SyncAccounts

WORKER_QUEUE = "mp:worker"

class Runner:

    thread = None

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe()
        self.pubsub.subscribe(**{WORKER_QUEUE: self.__fetch_jobs})

    def run(self):
        self.thread = self.pubsub.run_in_thread(sleep_time=0.1)

    def __fetch_jobs(self):
        message = self.pubsub.get_message()
        if message is not None:
            job = message['job']
            if job is not None:
                # todo - figure out some way to dynamically dispatch this
                if job == 'account_sync':
                    job = SyncAccounts(message)