from marshmallow import Schema, fields

from core.models import HoldingBalance
from api.lib.globals import marshmallow_app as ma


class ReadHoldingBalanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HoldingBalance
        include_fk = True

read_holding_balance_schema = ReadHoldingBalanceSchema()
read_holding_balances_schema = ReadHoldingBalanceSchema(many=True)