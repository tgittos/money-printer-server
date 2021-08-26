from .plaid import oauth_bp


def init_app(app):
    print(" * registering plaid oauth blueprint")
    app.register_blueprint(oauth_bp)
