from marshmallow import Schema, fields


class CreateProfileSchema(Schema):
    class Meta:
        fields = ("email", "password", "first_name", "last_name")


class ReadProfileSchema(Schema):
    accounts: fields.Nested('ReadAccountSchema', many=True)
    plaid_items: fields.Nested('ReadPlaidItemSchema', many=True)
    api_keys: fields.Nested('ReadApiKeySchema', many=True)

    class Meta:
        additional = ("id", "email", "first_name", "last_name",
                      "is_demo_profile", "timestamp")


class UpdateProfileSchema(Schema):
    class Meta:
        fields = ("id", "first_name", "last_name")
