import os
import sys
import signal

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from config import config, mysql_config, mailgun_config
from core.repositories.profile_repository import get_repository as get_profile_repository, RegisterProfileRequest
from core.lib.logger import init_logger, get_logger

from .routes.plaid import oauth_bp as plaid_bp
from .routes.auth import auth_bp
from .routes.accounts import account_bp
from .routes.symbols import symbol_bp
from .routes.webhooks import webhooks_bp
from .lib.client_bus import ClientBus


class ApiApplication:

    log_path = os.path.dirname(__file__) + "/../../../logs/"
    flask_app = Flask(__name__)
    socket_app = None
    client_bus = None

    def __init__(self):
        init_logger(self.log_path)
        self.logger = get_logger("server.services.api")
        self._configure_flask()
        self._configure_ws()

    def run(self):
        print(" * Starting money-printer api/ws application", flush=True)
        self.client_bus.start()
        self.socket_app.run(self.flask_app, host=config.host, port=config.port)

    def init(self, first_name, last_name, email):
        repo = get_profile_repository(mysql_config=mysql_config, mailgun_config=mailgun_config)
        result = repo.register(RegisterProfileRequest(
            email=email, first_name=first_name, last_name=last_name
        ))
        return result

    def _configure_flask(self):
        self.logger.debug("configuring base Flask application")
        self.flask_app.config['CORS_HEADERS'] = 'Content-Type'
        self.flask_app.config['SECRET_KEY'] = config.secret
        self.flask_app.url_map.strict_slashes = False
        CORS(self.flask_app)
        self._configure_routes()

    def _configure_routes(self):
        self.logger.info("registering auth blueprint")
        self.flask_app.register_blueprint(auth_bp)
        self.logger.info("registering plaid oauth blueprint")
        self.flask_app.register_blueprint(plaid_bp)
        self.logger.info("registering accounts blueprint")
        self.flask_app.register_blueprint(account_bp)
        self.logger.info("registering symbol blueprint")
        self.flask_app.register_blueprint(symbol_bp)
        self.logger.info("registering webhook blueprint")
        self.flask_app.register_blueprint(webhooks_bp)

    def _configure_ws(self):
        self.logger.debug("configuring SocketIO ws")
        self.socket_app = SocketIO(self.flask_app,
                                   cors_allowed_origins='*',
                                   message_queue="redis://")
        self.client_bus = ClientBus(self.socket_app)

    def _configure_signals(self):
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
