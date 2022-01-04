from marshmallow import Schema, fields

from core.models import HoldingBalance


class CreateHoldingBalanceSchema(Schema):
    class Meta:
        fields = ("holding_id", "cost_basis", "quantity")


class UpdateHoldingBalanceSchema(Schema):
    class Meta:
        fields = ("id", "cost_basis", "quantity")
