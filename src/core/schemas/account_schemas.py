from marshmallow import Schema, fields


class CreateAccountSchema(Schema):
    class Meta:
        fields = ("account_id", "name", "official_name", "type", "subtype")


class ReadAccountSchema(Schema):
    profile = fields.Nested('ReadProfileSchema', exclude=("accounts", "plaid_items", "api_keys"))
    plaid_item = fields.Nested('ReadPlaidItemSchema', exclude=("profile", "accounts"))
    balances = fields.Nested('ReadAccountBalanceSchema', many=True)
    holdings = fields.Nested('ReadHoldingSchema', many=True, exclude=
        ("account", "balances"))
    transactions = fields.Nested('ReadInvestmentTransactionSchema', many=True)

    class Meta:
        additional = ("id", "profile_id", "plaid_item_id", "name", "official_name",
                      "type", "subtype", "timestamp")


read_account_schema = ReadAccountSchema(exclude=("profile", "plaid_item", "balances", "holdings", "transactions"))
read_accounts_schema = ReadAccountSchema(many=True, exclude=("profile", "plaid_item", "balances", "holdings", "transactions"))
read_account_with_financials_schema = ReadAccountSchema(exclude=("profile", "plaid_item"))
read_accounts_with_financials_schema = ReadAccountSchema(many=True, exclude=("profile", "plaid_item"))


class UpdateAccountSchema(Schema):
    class Meta:
        fields = ("id", "account_id", "name",
                  "official_name", "type", "subtype")


class CreateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("account_id", "available", "current", "iso_currency_code")


class ReadAccountBalanceSchema(Schema):
    account = fields.Nested('ReadAccountSchema', exclude=("profile", "plaid_item", "balances", "holdings", "transactions"))

    class Meta:
        additional = ("id", "account_id", "available", "current",
                      "iso_currency_code", "timestamp")


class UpdateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("id", "available", "current")
