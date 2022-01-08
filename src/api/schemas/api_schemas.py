from marshmallow import Schema, fields

from core.models import ApiToken, ApiTokenPolicy
from api.flask_app import ma


class ReadApiTokenApiSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ApiToken
        include_fk = True


class ReadApiTokenPolicyApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApiTokenPolicy
        include_fk = True

read_api_token_schema = ReadApiTokenApiSchema()
read_api_tokens_schema = ReadApiTokenApiSchema(many=True)

read_api_token_policy_schema = ReadApiTokenPolicyApiSchema()
read_api_token_policies_schema = ReadApiTokenPolicyApiSchema(many=True)