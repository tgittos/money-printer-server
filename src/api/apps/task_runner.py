import os
import sys
import traceback

import redis
from rq import Connection, Worker

from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.lib.logger import init_logger, get_logger
from core.lib.constants import WORKER_QUEUE
from config import redis_config


class TaskRunnerApplication:

    log_path = os.path.dirname(__file__) + "/../../../logs/"
    worker = None

    def __init__(self):
        init_logger(os.path.dirname(__file__) + "/../../../logs/")
        self.logger = get_logger("server.services.task_runner")
        self.r = redis.Redis(host=redis_config.host, port=redis_config.port, db=0)

    def run(self):
        print(" * Starting money-printer task runner application", flush=True)
        print(" * Ensuring persistent jobs scheduled", flush=True)
        repo = ScheduledJobRepository()
        repo.schedule_persistent_jobs()
        q = sys.argv[1:] or [WORKER_QUEUE]
        print(" * Starting worker on queue/s {0}".format(q), flush=True)
        with Connection(self.r):
            self.worker = Worker(q)
            self.worker.work()

    def _handle_thread_error(self):
        self.logger.exception("exception in thread: {0}".format(traceback.format_exc()))
