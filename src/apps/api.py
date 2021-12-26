import os
import sys
import signal
import traceback

from flask import Flask, abort
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_graphql import GraphQLView
import rq_dashboard
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

from config import config, redis_config, env

from core.repositories.profile_repository import ProfileRepository
from core.schemas.auth_schemas import RegisterProfileSchema
from core.lib.logger import init_logger, get_logger

from api.routes.plaid import oauth_bp as plaid_bp
from api.routes.auth import auth_bp
from api.routes.accounts import account_bp
from api.routes.symbols import symbol_bp
from api.routes.webhooks import webhooks_bp
from api.routes.health import health_bp
from api.routes.profile import profile_bp
from api.routes.scheduler import scheduler_bp
from api.routes.swagger import swagger_bp

from api.graphql.schema import schema
from api.lib.client_bus import ClientBus
from api.lib.constants import API_PREFIX


class ApiApplication:

    log_path = os.path.dirname(__file__) + "/../../logs/"
    flask_app = None
    socket_app = None
    client_bus = None
    store = None
    configured = False

    def __init__(self, store):
        init_logger(self.log_path)
        self.logger = get_logger("server.services.api")
        self.store = store
        self.flask_app = Flask(__name__)
        self._configure_flask()
        self._configure_ws()
        # override RQ redis url
        self.flask_app.config["RQ_DASHBOARD_REDIS_URL"] = "redis://{0}:{1}".format(
            redis_config.host,
            redis_config.port
        )
        self.configured = True

    def run(self):
        print(" * Starting money-printer api/ws application", flush=True)
        self.client_bus.start()
        self.flask_app.run(host=config.host, port=config.port)
        self.socket_app.run(self.flask_app, host=config.host, port=config.port)

    def init(self, first_name, last_name, email):
        repo = ProfileRepository(self.store)
        result = repo.register(RegisterProfileSchema(
            email=email, first_name=first_name, last_name=last_name
        ))
        return result

    def _configure_flask(self):
        if self.configured:
            return
        self.logger.debug("configuring base Flask application")
        self.flask_app.config['CORS_HEADERS'] = 'Content-Type'
        self.flask_app.config['SECRET_KEY'] = config.secret
        CORS(self.flask_app)
        self.flask_app.handle_exception = self._rescue_exceptions
        self.flask_app.config.from_object(rq_dashboard.default_settings)
        self._configure_graphql()
        self._configure_prometheus()
        self._configure_routes()

    def _configure_routes(self):
        if self.configured:
            return
        self.logger.info("registering rq blueprint")
        self.flask_app.register_blueprint(
            rq_dashboard.blueprint, url_prefix="/rq")
        self.logger.info("registering health blueprint")
        self.flask_app.register_blueprint(health_bp)
        self.logger.info("registering auth blueprint")
        self.flask_app.register_blueprint(auth_bp)
        self.logger.info("registering plaid oauth blueprint")
        self.flask_app.register_blueprint(plaid_bp)
        self.logger.info("registering profile blueprint")
        self.flask_app.register_blueprint(profile_bp)
        self.logger.info("registering accounts blueprint")
        self.flask_app.register_blueprint(account_bp)
        self.logger.info("registering symbol blueprint")
        self.flask_app.register_blueprint(symbol_bp)
        self.logger.info("registering webhook blueprint")
        self.flask_app.register_blueprint(webhooks_bp)
        self.logger.info("registering scheduler blueprint")
        self.flask_app.register_blueprint(scheduler_bp)
        self.logger.info("registering swagger docs blueprint")
        self.flask_app.register_blueprint(swagger_bp)

    def _configure_ws(self):
        if self.configured:
            return
        self.logger.debug("configuring SocketIO ws")
        self.socket_app = SocketIO(self.flask_app,
                                   cors_allowed_origins='*',
                                   message_queue="redis://")
        self.client_bus = ClientBus(self.socket_app)

    def _configure_prometheus(self):
        if self.configured:
            return
        self.logger.debug("configuring Prometheus metrics endpoint")
        self.flask_app.wsgi_app = DispatcherMiddleware(self.flask_app.wsgi_app, {
            '/v1/api/metrics': make_wsgi_app()
        })

    def _configure_graphql(self):
        if self.configured:
            return
        self.logger.debug("configuring GraphQL endpoint")
        in_prod = 'MP_ENVIRONMENT' in os.environ and os.environ['MP_ENVIRONMENT'] == "production"
        self.flask_app.add_url_rule(
            f"/{API_PREFIX}/graphql",
            view_func=GraphQLView.as_view(
                'graphql_view',
                schema=schema,
                graphiql=not in_prod,
                header_editor_enabled=not in_prod,
                should_persist_headers=not in_prod
            )
        )

    def _rescue_exceptions(self, ex: Exception):
        error_json = {
            'error': ex,
        }
        if env != 'production':
            # apparently traceback can throw an exception ¯\_(ツ)_/¯
            try:
                error_json['traceback'] = traceback.format_exc(ex)
            except Exception as ex:
                error_json['traceback'] = ex
        self.logger.exception(
            "uncaught exception from Flask app: {0}".format(error_json))
        abort(500, error_json)

    def _configure_signals(self):
        if self.configured:
            return
        self.logger.debug("intercepting sigints for graceful shutdown")
        signal.signal(signal.SIGINT, self._curry_sigint_handler({
            "client_bus": self.client_bus
        }))

    def _curry_sigint_handler(self, context):
        client_bus = context["client_bus"]

        def sigint_handler(signal, frame):
            self.logger.info("requested api shutdown")
            if client_bus:
                client_bus.stop()
            sys.exit(0)

        return sigint_handler
