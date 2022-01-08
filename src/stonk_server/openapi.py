import json
from os import sync
from flask.views import MethodView
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from core.schemas import *
from core.lib.logger import get_logger

from .schemas import *


def write_apispec(path, app):
    spec = APISpec(
        title="Money Printer Stonks API",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="The Money Printer stock price repository and data server"),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    # security
    # api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
    jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

    # spec.components.security_scheme("api_key", api_key_scheme)
    spec.components.security_scheme("jwt", jwt_scheme)

    # paths
    with app.test_request_context():
        for name, view in app.view_functions.items():
            spec.path(view=view)

    with open(path, 'w') as f:
        f.write(json.dumps(spec.to_dict()))
