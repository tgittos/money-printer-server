from marshmallow import Schema, fields


class CreateAccountSchema(Schema):
    class Meta:
        fields = ("plaid_item_id", "profile_id", "account_id",
                  "name", "official_name", "type", "subtype")


class ReadAccountSchema(Schema):
    profile = fields.Nested('ReadProfileSchema', exclude=("account",))
    plaid_item = fields.Nested('ReadPlaidItemSchema', exclude=("account",))
    balances = fields.Nested('ReadAccountBalanceSchema',
                             many=True, exclude=("account",))
    holdings = fields.Nested(
        'ReadHoldingSchema', many=True, exclude=("account",))
    transactions = fields.Nested(
        'ReadInvestmentTransactionSchema', many=True, exclude=("account",))

    class Meta:
        additional = ("id", "plaid_item_id", "profile_id", "account_id",
                      "name", "official_name", "type", "subtype", "timestamp")


class UpdateAccountSchema(Schema):
    class Meta:
        fields = ("profile_id", "id", "account_id", "name",
                  "official_name", "type", "subtype")


class CreateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("account_id", "available", "current", "iso_currency_code")


class ReadAccountBalanceSchema(Schema):
    account = fields.Nested('ReadAccountSchema', exclude=('balances',))

    class Meta:
        additional = ("id", "account_id", "available", "current",
                      "iso_currency_code", "timestamp")


class UpdateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("id", "available", "current")
