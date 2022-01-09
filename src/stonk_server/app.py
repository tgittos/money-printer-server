import os
import signal
import sys

from stonk_server.flask_app import app, sse
from stonk_server.views import health_bp, swagger_bp, prices_bp
from stonk_server.openapi import write_apispec
from stonk_server import logger

from config import config

def create_app(flask_config={}):

    # configure the app
    logger.debug("registering health endpoints")
    app.register_blueprint(health_bp)
    logger.debug("registering swagger endpoint")
    app.register_blueprint(swagger_bp)
    logger.debug("registering prices endpoints")
    app.register_blueprint(prices_bp)

    logger.debug("intercepting sigints for graceful shutdown")
    signal.signal(signal.SIGINT, sigint_handler)

    return (app, sse)


def sigint_handler(signal, frame):
    print(" * requested stonk server shutdown", flush=True)
    if sse:
        logger.info("shutting down sse client")
        sse.stop()
    sys.exit(0)


if __name__ == '__main__':
    app, sse = create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']
        if os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
            doc_path = os.path.dirname(__file__) + "/docs/swagger/"
            write_apispec(doc_path + "swagger.json", app)

    print(" * Starting money-printer stonk server", flush=True)
    app.run(host=config.host, port=config.port)
    logger.info("starting sse client")
    sse.start()
    logger.info("starting client bus")
