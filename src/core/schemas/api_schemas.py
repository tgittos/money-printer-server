from marshmallow import Schema, fields

from core.models import ApiToken, ApiTokenPolicy


class CreateApiTokenSchema(Schema):
    class Meta:
        fields = ("profile_id",)


class UpdateApiTokenSchema(Schema):
    class Meta:
        fields = ("id", "status", "api_token_policy_id")


class CreateApiTokenPolicySchema():
    class Meta:
        model = ApiTokenPolicy


class UpdateApiTokenPolicySchema():
    class Meta:
        fields = ("id", "doc", "hosts")
