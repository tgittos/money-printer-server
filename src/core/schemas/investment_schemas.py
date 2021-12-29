from marshmallow import Schema, fields


class CreateInvestmentTransactionSchema(Schema):
    class Meta:
        fields = ("account_id", "name", "amount", "feeds", "price", "quantity", "date",
                  "investment_transaction_id", "iso_currency_code", "type", "subtype")


class ReadInvestmentTransactionSchema(Schema):
    account = fields.Nested('ReadAccountSchema')

    class Meta:
        additional = ("id", "account_id", "name", "amount", "feeds", "price", "quantity", "date",
                      "investment_transaction_id", "iso_currency_code", "type", "subtype", "timestamp")


class UpdateInvestmentTransactionSchema(Schema):
    class Meta:
        fields = ("id", "name", "amount", "feeds", "price", "quantity", "date",
                  "investment_transaction_id", "iso_currency_code", "type", "subtype")
