import os
import traceback
import time

from core.lib.logger import init_logger, get_logger

from .lib.runner import Runner
from .lib.worker import Worker


class TaskRunnerApplication:

    log_path = os.path.dirname(__file__) + "/../../../logs/"

    def __init__(self):
        init_logger(os.path.dirname(__file__) + "/../../../logs/")
        self.logger = get_logger("server.services.task_runner")
        self.runner_thread = Runner()
        self.worker_thread = Worker()

    def run(self):
        print(" * Starting money-printer task runner application", flush=True)
        self.worker_thread.start()
        self.runner_thread.start()
        while True:
            time.sleep(0.2)

    def _configure_thread_error_handlers(self):
        self.worker_thread.on_error = self._handle_thread_error
        self.runner_thread.on_error = self._handle_thread_error

    def _handle_thread_error(self):
        self.logger.exception("exception in thread: {0}".format(traceback.format_exc()))
