import os

from flask import Flask, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_graphql import GraphQLView
import rq_dashboard
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from flask_marshmallow import Marshmallow

from core.repositories.profile_repository import ProfileRepository
from core.schemas.auth_schemas import RegisterProfileSchema
from core.lib.logger import init_logger, get_logger

from api.lib.client_bus import ClientBus
from api.lib.constants import API_PREFIX
from api.lib.apispec import write_apispec
from api.views import register_api, register_swagger
from config import config

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.api")

if 'MP_ENVIRONMENT' in os.environ:
    os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']

logger.debug("* initializing Flask, Marshmallow and Client Bus")
app = Flask(__name__)
ma = Marshmallow(app)
ws = SocketIO(app, cors_allowed_origins='*', message_queue="redis://")
cb = ClientBus(ws)

configured = False

# create the app
def create_app(flask_config={}):
    global app, ma, configured

    if configured:
        return (app, ma, cb, ws)

    in_prod = 'MP_ENVIRONMENT' in os.environ and os.environ['MP_ENVIRONMENT'] == "production"

    logger.debug("* configuring base Flask application")
    _configure_flask(app, flask_config)

    logger.debug("* configuring GraphQL endpoint")
    _configure_graphql(app, in_prod=in_prod)

    logger.debug("* configuring Prometheus metrics endpoint")
    _configure_prometheus(app)

    logger.info("* registering rq blueprint")
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

    logger.debug("* registering all API routes with the app")
    register_api(app)

    if not in_prod:
        logger.debug("* registering SwaggerUI endpoint")
        register_swagger(app)

    configured = True

    return (app, ma, cb, ws)


def _configure_flask(app, flask_config):
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = config.secret
    CORS(app)
    app.config.from_object(flask_config)
    app.config.from_object(rq_dashboard.default_settings)


def _configure_graphql(app, in_prod=True):
    from api.graphql.schema import schema
    if 'graphql_view' not in app.view_functions:
        app.add_url_rule(
            f"/{API_PREFIX}/graphql",
            view_func=GraphQLView.as_view(
                'graphql_view',
                schema=schema,
                graphiql=not in_prod,
                header_editor_enabled=not in_prod,
                should_persist_headers=not in_prod
            )
        )

def _configure_prometheus(app):
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/v1/api/metrics': make_wsgi_app()
    })


def run():
    print(" * Starting money-printer api/ws application", flush=True)
    cb.start()
    app.run(host=config.host, port=config.port)
    ws.run(app, host=config.host, port=config.port)


def init(first_name, last_name, email):
    repo = ProfileRepository()
    result = repo.register(RegisterProfileSchema(
        email=email, first_name=first_name, last_name=last_name
    ))
    return result


if __name__ == '__main__':

    # create the app
    app, ma, cb, ws = create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']
        if os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
            doc_path = os.path.dirname(__file__) + "/../../docs/swagger/"
            write_apispec(doc_path + "swagger.json", app)
    
    # always run on the public port, cause we're in a container
    app.run(host='0.0.0.0')