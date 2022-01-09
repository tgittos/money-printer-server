from marshmallow import Schema, fields

from core.models import Holding


class CreateHoldingSchema(Schema):
    class Meta:
        fields = ("account_id", "symbol", "cost_basis",
                  "quantity", "iso_currency_code")


class UpdateHoldingSchema(Schema):
    class Meta:
        fields = ("id", "cost_basis", "quantity", "iso_currency_code")
