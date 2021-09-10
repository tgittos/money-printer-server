from .plaid import oauth_bp
from .auth import auth_bp
from .symbols import symbol_bp


def init_app(app):
    print(" * registering auth blueprint")
    app.register_blueprint(auth_bp)
    print(" * registering plaid oauth blueprint")
    app.register_blueprint(oauth_bp)
    print(" * registering symbol blueprint")
    app.register_blueprint(symbol_bp)
