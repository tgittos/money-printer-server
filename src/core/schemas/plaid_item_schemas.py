from marshmallow import Schema, fields


class CreatePlaidItemSchema(Schema):
    profile_id = fields.Int(required=True)
    item_id = fields.Str()
    access_token = fields.Str(required=True)
    request_id = fields.Str()
    status = fields.Str()


class ReadPlaidItemSchema(Schema):
    profile = fields.Nested('ReadProfileSchema', exclude=('plaid_items',))
    accounts = fields.Nested(
        'ReadAccountSchema', many=True, exclude=("plaid_item",))

    class Meta:
        additional = ("id", "profile_id", "item_id",
                      "request_id", "status", "timestamp")


class UpdatePlaidItemSchema(Schema):
    id = fields.Int(required=True)
    status = fields.Str()
