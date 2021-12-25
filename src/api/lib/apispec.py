import json
from os import sync
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from core.schemas.create_schemas import *
from core.schemas.update_schemas import *
from core.schemas.request_schemas import *

from api.apps.api import ApiApplication
from api.routes.profile import *
from api.routes.auth import *

spec = APISpec(
    title="Money Printer",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="An API to make money"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# schemas
spec.components.schema("RequestRegistration", schema=RequestRegistrationSchema)
spec.components.schema("RequestPasswordReset",
                       schema=RequestPasswordResetSchema)
spec.components.schema("RequestAuth", schema=RequestAuthSchema)

spec.components.schema("ReadProfile", schema=ReadProfileSchema)

spec.components.schema("UpdateProfile", schema=UpdateProfileSchema)

# paths
with ApiApplication(None).flask_app.test_request_context():
    # auth
    spec.path(view=register)
    spec.path(view=login)
    spec.path(view=reset_password)
    spec.path(view=continue_reset_password)

    # profile
    spec.path(view=get_profile)
    spec.path(view=update_profile)
    spec.path(view=sync_profile)


def write_apispec(path):
    with open(path, 'w') as f:
        f.write(json.dumps(spec.to_dict()))
