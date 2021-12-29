from marshmallow import Schema, fields


class CreateAccountSchema(Schema):
    class Meta:
        fields = ("account_id", "name", "official_name", "type", "subtype")


class ReadAccountSchema(Schema):
    profile = fields.Nested('ReadProfileSchema')
    plaid_item = fields.Nested('ReadPlaidItemSchema')
    balances = fields.Nested('ReadAccountBalanceSchema', many=True)
    holdings = fields.Nested('ReadHoldingSchema', many=True)
    transactions = fields.Nested('ReadInvestmentTransactionSchema', many=True)

    class Meta:
        additional = ("id", "name", "official_name",
                      "type", "subtype", "timestamp")


class UpdateAccountSchema(Schema):
    class Meta:
        fields = ("id", "account_id", "name",
                  "official_name", "type", "subtype")


class CreateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("account_id", "available", "current", "iso_currency_code")


class ReadAccountBalanceSchema(Schema):
    account = fields.Nested('ReadAccountSchema')

    class Meta:
        additional = ("id", "account_id", "available", "current",
                      "iso_currency_code", "timestamp")


class UpdateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("id", "available", "current")
