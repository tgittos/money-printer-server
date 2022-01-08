import os
import signal
import sys

from config import config

from stonk_server.flask_app import app, sse
from stonk_server.views import prices_bp
from stonk_server.api import write_apispec

from stonk_server import logger

def create_app(flask_config={}):

    # configure the app

    logger.debug("registering prices endpoints")
    app.register_blueprint(prices_bp)

    logger.debug("intercepting sigints for graceful shutdown")
    signal.signal(signal.SIGINT, sigint_handler)


def sigint_handler(signal, frame):
    print(" * requested stonk server shutdown", flush=True)
    if sse:
        logger.info("shutting down sse client")
        sse.stop()
    sys.exit(0)


def run():
    print(" * Starting money-printer stonk server", flush=True)
    logger.info("starting sse client")
    sse.start()
    logger.info("starting client bus")
    app.start(host=config.host, port=config.port)


if __name__ == '__main__':
    create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']
        if os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
            doc_path = os.path.dirname(__file__) + "/../../docs/swagger/"
            write_apispec(doc_path + "swagger.stonks.json", app)

    run()