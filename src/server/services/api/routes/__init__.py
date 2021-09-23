from .plaid import oauth_bp
from .auth import auth_bp
from .accounts import account_bp
from .symbols import symbol_bp
from .webhooks import webhooks_bp

from core.lib.logger import get_logger


def init_app(app):
    logger = get_logger('server.services.api.routes')
    logger.info("registering auth blueprint")
    app.register_blueprint(auth_bp)
    logger.info("registering plaid oauth blueprint")
    app.register_blueprint(oauth_bp)
    logger.info("registering accounts blueprint")
    app.register_blueprint(account_bp)
    logger.info("registering symbol blueprint")
    app.register_blueprint(symbol_bp)
    logger.info("registering webhook blueprint")
    app.register_blueprint(webhooks_bp)
