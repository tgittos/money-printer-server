import time
import os
import signal
import sys

from flask import Flask, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow

from core.lib.logger import init_logger, get_logger
from config import config, env

from core.lib.client_bus import ClientBus
from .lib.sse_client import SSEClient
from .lib.historical_client import HistoricalClient
from .rest.blueprints import prices_bp

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.stonk_server")

if 'MP_ENVIRONMENT' in os.environ:
    os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']

logger.debug("* initializing Flask, Marshmallow and Client Bus")
app = Flask(__name__)
ma = Marshmallow(app)
cb = ClientBus()
sse_client = SSEClient(env, config.iex.secret)
historical_client = HistoricalClient()


def create_app(flask_config={}):

    logger.debug("registering prices endpoints")
    app.register_blueprint(prices_bp)

    logger.debug("intercepting sigints for graceful shutdown")
    signal.signal(signal.SIGINT, sigint_handler({
        "sse_client": sse_client,
        "historical_client": historical_client
    }))


def sigint_handler(signal, frame):
    print("requested data-server shutdown", flush=True)
    if sse_client:
        print("shutting down sse client", flush=True)
        sse_client.stop()
    if historical_client:
        print("shutting down historical client", flush=True)
        historical_client.stop()
    sys.exit(0)


def run():
    print(" * Starting money-printer data server", flush=True)
    logger.info("starting sse client")
    sse_client.start()
    logger.info("starting historical client")
    historical_client.start()
    # block until a stop is requested, sigint handler should handle the
    # all thread shutdowns
    while True:
        time.sleep(1)


if __name__ == '__main__':
    app, ma, ws = create_app()
    app.run()