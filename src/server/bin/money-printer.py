import threading

from server.services.data_server.application import DataServerApplication
from server.services.task_runner.application import TaskRunnerApplication
from server.services.api.application import ApiApplication

if __name__ == '__main__':
    data = DataServerApplication()
    api = ApiApplication()
    runner = TaskRunnerApplication()

    data_thread = threading.Thread(target=data.run)
    runner_thread = threading.Thread(target=runner.run)
    api_thread = threading.Thread(target=api.run)

    data_thread.start()
    runner_thread.start()
    api_thread.start()

    data_thread.join()
    runner_thread.join()
    api_thread.join()
