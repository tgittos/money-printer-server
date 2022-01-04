from marshmallow import Schema, fields

from core.models import ApiToken, ApiTokenPolicy
from api.lib.globals import marshmallow_app as ma


class ReadApiTokenSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ApiToken
        include_fk = True


class ReadApiTokenPolicySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApiTokenPolicy
        include_fk = True

read_api_token_schema = ReadApiTokenSchema()
read_api_tokens_schema = ReadApiTokenSchema(many=True)

read_api_token_policy_schema = ReadApiTokenPolicySchema()
read_api_token_policies_schema = ReadApiTokenPolicySchema(many=True)