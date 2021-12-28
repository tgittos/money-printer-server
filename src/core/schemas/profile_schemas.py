from marshmallow import Schema, fields


class CreateProfileSchema(Schema):
    class Meta:
        fields = ("email", "password", "first_name", "last_name")


class ReadProfileSchema(Schema):
    account: fields.Nested('ReadAccountSchema', exclude=("profile",))
    plaid_item: fields.Nested('ReadPlaidItemSchema', exclude=("profile",))
    api_keys: fields.Nested('ReadApiKeySchema', exclude=("profile",))

    class Meta:
        additional = ("id", "email", "first_name", "last_name",
                      "is_demo_profile", "timestamp")


class UpdateProfileSchema(Schema):
    class Meta:
        fields = ("id", "first_name", "last_name")
