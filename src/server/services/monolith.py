import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import traceback


def curry_sigint_handler(context):
    def sigint_handler(signal, frame):
        context['sse'].join()
        context['historical'].join()
        context['runner'].join()
        context['worker'].join()
        sys.exit(0)
    return sigint_handler


def handle_thread_error(ex):
    logger.exception("exception in thread: {0}".format(traceback.format_exc()))


if __name__ == '__main__':
    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../../")

    # set the current dir to our project root
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    sys.path.append(pwd)

    # configure the logger
    from server.config import config, env
    from core.lib.logger import init_logger, get_logger
    init_logger(os.path.dirname(__file__) + "/../../../logs/")

    # grab a ref to the logger
    logger = get_logger("server.services.api")

    # log all the previous stuff we set up
    logger.debug("setting env to {0}".format(env))
    logger.debug("changing pwd to {0}".format(pwd))
    logger.debug("augmented path with core")
    logger.debug("path: {0}".format(sys.path))

    # base flask app
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.url_map.strict_slashes = False
    CORS(app)

    # client bus
    from server.services.client_bus.client_bus import ClientBus
    socket_app = SocketIO(app, cors_allowed_origins='*', message_queue="redis://{0}".format(config.redis.host))

    logger.debug("augmenting money-printer websocket server with message handlers")
    client_bus = ClientBus(socket_app)

    # data server
    from server.services.data_server.sse_client import SSEClient
    from server.services.data_server.historical_client import HistoricalClient

    sse_client = SSEClient(env, config.iex.secret)
    logger.debug("sse upstream online")

    historical_client = HistoricalClient()
    logger.debug("historical upstream online")

    logger.info("running money-printer data server")

    # task runner
    from server.services.task_runner.runner import Runner
    from server.services.task_runner.worker import Worker

    runner_thread = Runner()
    worker_thread = Worker()

    worker_thread.on_error = handle_thread_error
    worker_thread.start()

    runner_thread.on_error = handle_thread_error
    runner_thread.start()

    # load routes
    import routes
    logger.info("loading api routes")
    routes.init_app(app)

    # wire up the sigint intercept
    signal.signal(signal.SIGINT, curry_sigint_handler(context={
        'sse': sse_client,
        'historical': historical_client,
        'runner': runner_thread,
        'worker': worker_thread
    }))

    # start flask server
    logger.info("running money-printer websocket server")
    socket_app.run(app)
    logger.info("running money-printer api server")
    app.run(host=config.host, port=config.port)
