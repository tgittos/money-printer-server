from marshmallow import Schema, fields

from core.models import AccountBalance
from api.lib.globals import marshmallow_app as ma


class ReadAccountBalanceApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountBalance
        include_fk = True

read_account_balance_schema = ReadAccountBalanceApiSchema()
read_account_balances_schema = ReadAccountBalanceApiSchema(many=True)