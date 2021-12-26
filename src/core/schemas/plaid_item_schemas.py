from marshmallow import Schema, fields


class CreatePlaidItemSchema(Schema):
    class Meta:
        fields = ("profile_id", "item_id",
                  "access_token", "request_id", "status")


class ReadPlaidItemSchema(Schema):
    profile = fields.Nested('ReadProfileSchema', exclude=('plaid_item',))
    accounts = fields.Nested(
        'ReadAccountSchema', many=True, exclude=("plaid_item",))

    class Meta:
        additional = ("id", "profile_id", "item_id",
                      "request_id", "status", "timestamp")


class UpdatePlaidItemSchema(Schema):
    class Meta:
        fields = ("id", "status")
