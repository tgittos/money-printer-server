import time
import os
import signal
import sys

from flask import Flask, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow

from core.lib.logger import init_logger, get_logger
from core.stores.database import Database
from config import config

from core.lib.client_bus import ClientBus

from stonk_server.sse_client import SSEClient

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.stonk_server")

if 'MP_ENVIRONMENT' in os.environ:
    os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']

logger.debug("* initializing Flask, Marshmallow and Client Bus")
app = Flask(__name__)
db = Database(config.stonks)
ma = Marshmallow(app)
cb = ClientBus()
sse_client = SSEClient(config.iex.secret)

from stonk_server.blueprints import prices_bp
from stonk_server.api import write_apispec

def create_app(flask_config={}):

    # configure the app
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = config.secret
    CORS(app)

    logger.debug("registering prices endpoints")
    app.register_blueprint(prices_bp)

    logger.debug("intercepting sigints for graceful shutdown")
    signal.signal(signal.SIGINT, sigint_handler)


def sigint_handler(signal, frame):
    print(" * requested stonk server shutdown", flush=True)
    if sse_client:
        logger.info("shutting down sse client")
        sse_client.stop()
    sys.exit(0)


def run():
    print(" * Starting money-printer stonk server", flush=True)
    logger.info("starting sse client")
    sse_client.start()
    logger.info("starting client bus")
    app.start(host=config.host, port=config.port)


if __name__ == '__main__':
    create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']
        if os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
            doc_path = os.path.dirname(__file__) + "/../../docs/swagger/"
            write_apispec(doc_path + "swagger.api.json", app)

    run()