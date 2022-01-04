import sys
import inspect

from .base import BaseApi
from .webhooks import webhooks_bp
from .health import health_bp
from .swagger import swagger_bp


def register_api(app):
    """
    Iterates through all available views and registers them with
    the application if they can be registered.
    """
    api_views = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for name, api_view in api_views:
        if api_view is not issubclass(BaseApi, api_view):
            next
        obj = api_views()
        if hasattr(obj, 'register_api'):
            obj.register_api(app)
    
    # Manually register a few lower level APIs we don't expose to the user
    app.register_blueprint(health_bp)
    
    # Manually register the webhook blueprint, since it's not a full Api class
    app.register_blueprint(webhooks_bp)


def register_swagger(app):
    """
    Registers urls for accessing SwaggerUI through the API
    """
    app.register_blueprint(swagger_bp)