from marshmallow import Schema, fields

from core.models import AccountBalance


class CreateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("account_id", "available", "current", "iso_currency_code")


class UpdateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("id", "available", "current")
