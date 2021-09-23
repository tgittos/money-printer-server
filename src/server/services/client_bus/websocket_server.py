#import eventlet
#eventlet.monkey_patch()

import os
import signal
import sys

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit


app = None
socket_app = None


def create_app():
    from server.config import config as server_config

    temp_app = Flask(__name__)

    # configure cores
    temp_app.config['CORS_HEADERS'] = 'Content-Type'
    temp_app.config['DEBUG'] = False
    CORS(temp_app)

    # global static configs
    temp_app.config['SECRET_KEY'] = server_config['server']['secret']

    return temp_app


def curry_sigint_handler(client_bus):
    def sigint_handler(signal, frame):
        logger.info("requested client-bus shutdown")
        # client_bus.unsubscribe_symbols
        sys.exit(0)
    return sigint_handler


if __name__ == '__main__':

    # echo the environment we're passing in
    env_string = os.environ['MONEY_PRINTER_ENV']

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
    logger = get_logger("websocket_server")

    # log all the previous stuff we set up
    logger.debug("setting env to {0}".format(env_string))
    logger.debug("changing pwd to {0}".format(pwd))
    logger.debug("augmented path with core")
    logger.debug("path: {0}".format(sys.path))

    # create the app
    from server.config import config as server_config
    from server.services.client_bus.client_bus import ClientBus

    app = create_app()
    socket_app = SocketIO(app, cors_allowed_origins='*', message_queue="redis://")

    logger.debug("augmenting money-printer websocket server with message handlers")
    client_bus = ClientBus(socket_app)

    # wire up the sigint intercept
    signal.signal(signal.SIGINT, curry_sigint_handler(client_bus=client_bus))

    logger.info("running money-printer websocket server")
    socket_app.run(app)
