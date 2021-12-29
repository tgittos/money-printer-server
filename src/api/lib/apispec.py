import json
from os import sync
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from core.schemas import *

from apps.api import ApiApplication
from api.routes.profile import *
from api.routes.auth import *
from api.routes.scheduler import *
from api.routes.accounts import *


spec = APISpec(
    title="Money Printer",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="An API to make money"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# security
# api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

# spec.components.security_scheme("api_key", api_key_scheme)
spec.components.security_scheme("jwt", jwt_scheme)

# schemas
spec.components.schema("RegisterProfile", schema=RegisterProfileSchema)
spec.components.schema("ResetPassword",
                       schema=ResetPasswordSchema)
spec.components.schema("Login", schema=LoginSchema)

spec.components.schema("ReadProfile", schema=ReadProfileSchema)
spec.components.schema("UpdateProfile", schema=UpdateProfileSchema)

spec.components.schema("CreateInstantJob", schema=CreateInstantJobSchema)
spec.components.schema("CreateScheduledJob", schema=CreateScheduledJobSchema)
spec.components.schema("ReadScheduledJob", schema=ReadScheduledJobSchema)
spec.components.schema("UpdateScheduledJob", schema=UpdateScheduledJobSchema)
spec.components.schema("ReadJobResult", schema=ReadJobResultSchema)

spec.components.schema("ReadAccount", schema=ReadAccountSchema)
spec.components.schema("CreateAccount", schema=CreateAccountSchema)
spec.components.schema("UpdateAccount", schema=UpdateAccountSchema)
spec.components.schema("CreateAccountBalance", schema=CreateAccountBalanceSchema)

spec.components.schema("ReadHolding", schema=ReadHoldingSchema)
spec.components.schema("CreateHolding", schema=CreateHoldingSchema)
spec.components.schema("UpdateHolding", schema=UpdateHoldingSchema)
spec.components.schema("CreateHoldingBalance", schema=CreateHoldingBalanceSchema)
spec.components.schema("UpdateHoldingBalance", schema=UpdateHoldingBalanceSchema)

spec.components.schema("ReadPlaidItem", schema=ReadPlaidItemSchema)

spec.components.schema("ReadInvestmentTransaction", schema=ReadInvestmentTransactionSchema)

spec.components.schema("ReadSecurity", schema=ReadSecuritySchema)
spec.components.schema("ReadSecurityPrice", schema=ReadSecurityPriceSchema)

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

    # accounts
    # spec.path(view=list_accounts)
    spec.path(view=request_account_sync)
    # spec.path(view=request_account_balances)
    # spec.path(view=list_holdings)

    # scheduler
    spec.path(view=list_schedules)
    spec.path(view=create_schedule)
    spec.path(view=update_schedule)
    spec.path(view=delete_schedule)


def write_apispec(path):
    with open(path, 'w') as f:
        f.write(json.dumps(spec.to_dict()))
