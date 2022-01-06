from marshmallow import Schema, fields

from core.models import Account


class CreateAccountSchema(Schema):
    class Meta:
        fields = ("account_id", "name", "official_name", "type", "subtype")


class UpdateAccountSchema(Schema):
    class Meta:
        fields = ("id", "account_id", "name",
                  "official_name", "type", "subtype")
