import os
import sys
import traceback

import redis
from rq import Connection, Worker

from core.stores.database import Database
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.lib.logger import init_logger, get_logger
from constants import WORKER_QUEUE
from config import config


class TaskRunnerApplication:

    log_path = os.path.dirname(__file__) + "/../logs/"
    worker = None
    db = Database(config.api)

    def __init__(self):
        init_logger(self.log_path)
        self.logger = get_logger("server.services.task_runner")
        self.r = redis.Redis(host=config.redis.host,
                             port=config.redis.port, db=0)

    def run(self):
        print(" * Starting money-printer task runner application", flush=True)
        print(" * Ensuring persistent jobs scheduled", flush=True)
        repo = ScheduledJobRepository(self.db)
        repo.schedule_persistent_jobs()
        q = sys.argv[1:] or [WORKER_QUEUE]
        print(" * Starting worker on queue/s {0}".format(q), flush=True)
        with Connection(self.r):
            self.worker = Worker(q)
            self.worker.work()

    def _handle_thread_error(self):
        self.logger.exception(
            "exception in thread: {0}".format(traceback.format_exc()))


if __name__ == '__main__':
    app = TaskRunnerApplication()
    app.run()