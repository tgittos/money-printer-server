import os
from flask import Flask, abort
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_graphql import GraphQLView
import rq_dashboard
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from flask_marshmallow import Marshmallow

from core.lib.logger import init_logger, get_logger
from api.routes import *
from api.lib.client_bus import ClientBus
from api.lib.constants import API_PREFIX
from config import config, redis_config, env

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.api")

flask_app = Flask(__name__)
marshmallow_app = Marshmallow(globals.flask_app)
socket_app = SocketIO(flask_app,
                      cors_allowed_origins='*',
                      message_queue="redis://")
client_bus = ClientBus(socket_app)

flask_app.config["RQ_DASHBOARD_REDIS_URL"] = "redis://{0}:{1}".format(
    redis_config.host,
    redis_config.port
)

logger.debug("configuring base Flask application")
flask_app.config['CORS_HEADERS'] = 'Content-Type'
flask_app.config['SECRET_KEY'] = config.secret
CORS(flask_app)
flask_app.config.from_object(rq_dashboard.default_settings)

logger.info("registering rq blueprint")
flask_app.register_blueprint(
    rq_dashboard.blueprint, url_prefix="/rq")
logger.info("registering health blueprint")
flask_app.register_blueprint(health_bp)
logger.info("registering auth blueprint")
flask_app.register_blueprint(auth_bp)
logger.info("registering plaid oauth blueprint")
flask_app.register_blueprint(oauth_bp)
logger.info("registering profile blueprint")
flask_app.register_blueprint(profile_bp)
logger.info("registering accounts blueprint")
flask_app.register_blueprint(account_bp)
logger.info("registering holdings blueprint")
flask_app.register_blueprint(holdings_bp)
logger.info("registering symbol blueprint")
flask_app.register_blueprint(symbol_bp)
logger.info("registering webhook blueprint")
flask_app.register_blueprint(webhooks_bp)
logger.info("registering scheduler blueprint")
flask_app.register_blueprint(scheduler_bp)
logger.info("registering swagger docs blueprint")
flask_app.register_blueprint(swagger_bp)