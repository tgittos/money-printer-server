from threading import Thread
import redis
import time
import json
import importlib

from core.lib.logger import get_logger
from config import redis_config


WORKER_QUEUE = "mp:worker"


class Worker(Thread):

    running = False
    on_error = None

    def __init__(self):
        super(Worker, self).__init__()
        self.logger = get_logger(__name__)
        self.redis = redis.Redis(host=redis_config.host, port=redis_config.port, db=0)
        self.pub_sub = self.redis.pubsub()
        self.pub_sub.subscribe(WORKER_QUEUE)

    def start(self) -> None:
        self.logger.debug("job worker server thread running")
        self.running = True
        super(Worker, self).start()

    def stop(self) -> None:
        self.logger.debug(" * shutting job worker thread down")
        self.running = False
        super(Worker, self).join()

    def run(self):
        while self.running:
            try:
                message = self.pub_sub.get_message(ignore_subscribe_messages=True)
                while message is not None:
                    self.logger.debug("found message on worker queue: {0}".format(message))
                    self.__fetch_jobs(message)
                    message = self.pub_sub.get_message()
                time.sleep(1)
            except redis.exceptions.ConnectionError:
                # redis backbone connection terminated, shut ourselves down
                self.logger.exception("backbone redis connection dropped, shutting down")
                self.running = False
            except Exception as ex:
                if self.on_error is not None:
                    self.on_error(ex)
                else:
                    self.logger.exception("caught exception but no handler defined, swallowing: {0}".format(ex))

    def __fetch_jobs(self, message):
        json_data = json.loads(message['data'])
        job = json_data['job']
        if job is not None:
            job = self.__resolve_job(job, json_data)
            if job is not None:
                job.run()
            else:
                self.logger.error("could not resolve requested job: {0}".format(job))

    def __resolve_job(self, job_name, args):
        try:
            package = job_name
            klass = job_name.title().replace('_', '')
            job_module = importlib.import_module('server.services.task_runner.jobs.' + package)
            job_klass = getattr(job_module, klass)
            if job_klass is not None:
                return job_klass(args)
        except Exception as ex:
            raise Exception("error resolving job {0}".format(job_name), ex)
