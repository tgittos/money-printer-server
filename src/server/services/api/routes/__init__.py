from .plaid import oauth_bp
from .auth import auth_bp


def init_app(app):
    print(" * registering plaid oauth blueprint")
    app.register_blueprint(oauth_bp)
    print(" * registering auth blueprint")
    app.register_blueprint(auth_bp)
