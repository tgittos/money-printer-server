import os

import rq_dashboard
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

from api.openapi import write_apispec
from api.views import register_api, register_swagger
from api.flask_app import app, ma
from api import logger

from constants import API_PREFIX
from config import config

# create the app
def create_app(flask_config={}):
    in_prod = 'MP_ENVIRONMENT' in os.environ and os.environ['MP_ENVIRONMENT'] == "production"

    logger.debug("* configuring base Flask application")
    _configure_flask(app, flask_config)

    logger.debug("* configuring Prometheus metrics endpoint")
    _configure_prometheus(app)

    logger.info("* registering rq blueprint")
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

    logger.debug("* registering all API routes with the app")
    register_api(app)

    if not in_prod:
        logger.debug("* registering SwaggerUI endpoint")
        register_swagger(app)

    return (app, ma)


def _configure_flask(app, flask_config):
    app.config.from_object(flask_config)
    app.config.from_object(rq_dashboard.default_settings)



def _configure_prometheus(app):
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/v1/api/metrics': make_wsgi_app()
    })


if __name__ == '__main__':
    # create the app
    app, ma = create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']
        if os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
            doc_path = os.path.dirname(__file__) + "/docs/swagger/"
            write_apispec(doc_path + "swagger.json", app)

    print(" * Starting money-printer api/ws application", flush=True)
    app.run(host=config.host, port=config.port)