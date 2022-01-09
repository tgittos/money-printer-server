from flask import current_app

from core.models import AccountBalance
from api.flask_app import ma


class ReadAccountBalanceApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountBalance
        include_fk = True

read_account_balance_schema = ReadAccountBalanceApiSchema()
read_account_balances_schema = ReadAccountBalanceApiSchema(many=True)