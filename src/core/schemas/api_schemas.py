from marshmallow import Schema, fields


class CreateApiKeySchema(Schema):
    class Meta:
        fields = ("profile_id")


class ReadApiKeySchema(Schema):
    policy: fields.Nested('ReadApiKeyPolicySchema')

    class Meta:
        additional = ("id", "profile_id", "status", "timestamp")


class UpdateApiKeySchema(Schema):
    class Meta:
        fields = ("id", "status", "api_token_policy_id")


class CreateApiKeyPolicySchema():
    class Meta:
        fields = ("doc", "hosts")


class ReadApiKeyPolicySchema():
    class Meta:
        fields = ("id", "doc", "hosts")


class UpdateApiKeyPolicySchema():
    class Meta:
        fields = ("id", "doc", "hosts")
    