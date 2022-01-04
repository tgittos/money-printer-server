from marshmallow import Schema, fields

from core.models import InvestmentTransaction


class CreateInvestmentTransactionSchema(Schema):
    class Meta:
        fields = ("account_id", "name", "amount", "feeds", "price", "quantity", "date",
                  "investment_transaction_id", "iso_currency_code", "type", "subtype")


class UpdateInvestmentTransactionSchema(Schema):
    class Meta:
        fields = ("id", "name", "amount", "feeds", "price", "quantity", "date",
                  "investment_transaction_id", "iso_currency_code", "type", "subtype")
