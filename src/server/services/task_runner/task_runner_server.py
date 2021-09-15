import os
import sys
import time


def handle_thread_error(ex):
    print(" * exception in thread: {0}".format(ex), flush=True)


if __name__ == '__main__':
    # echo the environment we're passing in
    env_string = os.environ['MONEY_PRINTER_ENV']
    print(" * setting env to {0}".format(env_string))

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../../")

    print(" * changing pwd to {0}".format(pwd))
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    print(" * augmenting path with core")
    sys.path.append(pwd)
    print(" * path: {0}".format(sys.path))

    from server.services.task_runner.runner import Runner
    from server.services.task_runner.worker import Worker

    runner_thread = Runner()
    worker_thread = Worker()

    print(" * starting real time worker thread", flush=True)
    worker_thread.on_error = handle_thread_error
    worker_thread.start()

    print(" * starting schedule runner thread", flush=True)
    runner_thread.on_error = handle_thread_error
    runner_thread.start()

    while True:
        time.sleep(1)

    print(" * shutting down worker, runner threads", flush=True)

    worker_thread.join()
    runner_thread.join()
