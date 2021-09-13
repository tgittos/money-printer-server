import redis
import json

from server.services.task_runner.jobs.sync_accounts import SyncAccounts

WORKER_QUEUE = "mp:worker"

class Runner:

    thread = None
    running = False

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(**{WORKER_QUEUE: self.__fetch_jobs})

    def run(self):
        # self.running = True
        self.thread = self.pubsub.run_in_thread(sleep_time=0.1)
        # while self.running:
        #     time.sleep(1)
        # self.thread.join()

    def __fetch_jobs(self, message):
        print(" * found message on worker queue: {0}".format(message))
        json_data = json.loads(message['data'])
        job = json_data['job']
        if job is not None:
            # todo - figure out some way to dynamically dispatch this
            if job == 'account_sync':
                print(" * syncing accounts for plaid access item")
                job = SyncAccounts(json_data)
                job.run()
