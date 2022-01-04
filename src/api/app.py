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

from config import config, redis_config, env


from api.views import register_api, register_swagger

# globals needed to hook things up, for example, schemas
app = Flask(__name__)
ma = Marshmallow(app)


# create the app
def create_app(store):
    in_prod = 'MP_ENVIRONMENT' in os.environ and os.environ['MP_ENVIRONMENT'] == "production"

    log_path = os.path.dirname(__file__) + "/../../logs/"
    init_logger(log_path)
    logger = get_logger("server.services.api")

    logger.debug("* initializing Flask and Marshmallow")

    logger.debug("* configuring base Flask application")
    _configure_flask(app)

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

    logger.debug("* configuring SocketIO ws")
    socket_app, client_bus = _configure_ws(app)


def _configure_flask(app):
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = config.secret
    CORS(app)
    # app.handle_exception = self._rescue_exceptions
    app.config.from_object(rq_dashboard.default_settings)


def _configure_ws(app):
    socket_app = SocketIO(app, cors_allowed_origins='*', message_queue="redis://")
    client_bus = ClientBus(socket_app)
    return (socket_app, client_bus)


def _configure_graphql(app, in_prod=True):
    from api.graphql.schema import schema
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
    app.wsgi_app = DispatcherMiddleware(globals.flask_app.wsgi_app, {
        '/v1/api/metrics': make_wsgi_app()
    })


def run(self):
    print(" * Starting money-printer api/ws application", flush=True)
    self.client_bus.start()
    self.flask_app.run(host=config.host, port=config.port)
    self.socket_app.run(globals.flask_app, host=config.host, port=config.port)


def init(self, first_name, last_name, email):
    repo = ProfileRepository(self.store)
    result = repo.register(RegisterProfileSchema(
        email=email, first_name=first_name, last_name=last_name
    ))
    return result