from marshmallow import Schema, fields

from core.models import PlaidItem


class CreatePlaidItemSchema(Schema):
    item_id = fields.Str()
    access_token = fields.Str(required=True)
    request_id = fields.Str()
    status = fields.Str()


class UpdatePlaidItemSchema(Schema):
    id = fields.Int(required=True)
    status = fields.Str()
