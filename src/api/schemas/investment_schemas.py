from marshmallow import Schema, fields

from core.models import InvestmentTransaction
from api.lib.globals import marshmallow_app as ma


class ReadInvestmentTransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InvestmentTransaction
        include_fk = True

read_investment_transaction_schema = ReadInvestmentTransactionSchema()
read_investment_transactions_schema = ReadInvestmentTransactionSchema(many=True)