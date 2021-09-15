from threading import Thread
import redis
import time
import json

from server.services.task_runner.jobs.sync_accounts import SyncAccounts


WORKER_QUEUE = "mp:worker"


class Worker(Thread):

    running = False
    on_error = None

    def __init__(self):
        super(Worker, self).__init__()
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.pub_sub = self.redis.pubsub()
        self.pub_sub.subscribe(WORKER_QUEUE)

    def start(self) -> None:
        print(" * worker thread running", flush=True)
        self.running = True
        super(Worker, self).start()

    def stop(self) -> None:
        print(" * shutting worker thread down", flush=True)
        self.running = False
        super(Worker, self).join()

    def run(self):
        while self.running:
            try:
                message = self.pub_sub.get_message(ignore_subscribe_messages=True)
                while message is not None:
                    print(" * found message on worker queue: {0}".format(message), flush=True)
                    self.__fetch_jobs(message)
                    message = self.pub_sub.get_message()
                time.sleep(1)
            except Exception as ex:
                if self.on_error is not None:
                    self.on_error(ex)
                else:
                    print(" * caught exception but no handler defined, swallowing: {0}".format(ex), flush=True)

    def __fetch_jobs(self, message):
        json_data = json.loads(message['data'])
        job = json_data['job']
        if job is not None:
            # todo - figure out some way to dynamically dispatch this
            if job == 'sync_accounts':
                print(" * syncing accounts for plaid access item", flush=True)
                job = SyncAccounts(json_data)
                job.run()
