import os
import sys
import time
import traceback


def handle_thread_error(ex):
    logger.exception("exception in thread: {0}".format(traceback.format_exc()))


if __name__ == '__main__':
    # echo the environment we're passing in
    env_string = os.environ['MP_ENVIRONMENT']

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../../")

    # set the current dir to our project root
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    sys.path.append(pwd)

    # configure the logger
    from core.lib.logger import init_logger, get_logger
    init_logger(os.path.dirname(__file__) + "/../../../logs/")

    # grab a ref to the logger
    logger = get_logger("server.services.task_runner")

    # log all the previous stuff we set up
    logger.debug("setting env to {0}".format(env_string))
    logger.debug("changing pwd to {0}".format(pwd))
    logger.debug("augmented path with core")
    logger.debug("path: {0}".format(sys.path))

    from server.services.task_runner.runner import Runner
    from server.services.task_runner.worker import Worker

    runner_thread = Runner()
    worker_thread = Worker()

    worker_thread.on_error = handle_thread_error
    worker_thread.start()

    runner_thread.on_error = handle_thread_error
    runner_thread.start()

    logger.info("running money-printer job server")

    while True:
        time.sleep(1)
