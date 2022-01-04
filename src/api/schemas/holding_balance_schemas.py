from marshmallow import Schema, fields

from core.models import HoldingBalance
from api.lib.globals import marshmallow_app as ma


class ReadHoldingBalanceApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HoldingBalance
        include_fk = True

read_holding_balance_schema = ReadHoldingBalanceApiSchema()
read_holding_balances_schema = ReadHoldingBalanceApiSchema(many=True)