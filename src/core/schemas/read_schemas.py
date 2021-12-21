from marshmallow import Schema, fields


class ReadSecurityPriceSchema(Schema):
    class Meta:
        fields = ("id", "symbol", "high", "low", "open", "close", "volume", \
            "u_high", "u_low", "u_open", "u_close", "u_volume", "date", "change", \
            "change_percent", "change_over_time", "resolution", "timestamp")

class ReadJobResultSchema(Schema):
    class Meta:
        fields = ("id", "job_id", "success", "log", "queue", "timestamp")


class ReadScheduledJobSchema(Schema):
    result = fields.Nested(ReadJobResultSchema)

    class Meta:
        additional = ("id", "cron", "job_name", "json_args", "last_run", "queue", "active", "timestamp")


class ReadIexBlacklistSchema(Schema):
    class Meta:
        fields = ("id", "symbol", "timestamp")


class ReadAccountSchema(Schema):
    profile = fields.Nested('ReadProfileSchema', exclude=("account",))
    plaid_item = fields.Nested('ReadPlaidItemSchema', exclude=("account",))
    balances = fields.Nested('ReadAccountBalanceSchema', many=True, exclude=("account",))
    holdings = fields.Nested('ReadHoldingSchema', many=True, exclude=("account",))
    transactions = fields.Nested('ReadInvestmentTransactionSchema', many=True, exclude=("account",))

    class Meta:
        additional = ("id", "plaid_item_id", "profile_id", "account_id", \
            "name", "official_name", "type", "subtype", "timestamp")


class ReadInvestmentTransactionSchema(Schema):
    account = fields.Nested('ReadAccountSchema', exclue=('transactions',))

    class Meta:
        additional = ("id", "account_id", "name", "amount", "feeds", "price", "quantity", "date",\
            "investment_transaction_id", "iso_currency_code", "type", "subtype", "timestamp")


class ReadAccountBalanceSchema(Schema):
    account = fields.Nested('ReadAccountSchema', exclude=('balances',))
    class Meta:
        additional = ("id", "account_id", "available", "current", "iso_currency_code", "timestamp")


class ReadPlaidItemSchema(Schema):
    profile = fields.Nested('ReadProfileSchema', exclude=('plaid_item',))
    accounts = fields.Nested(ReadAccountSchema, many=True, exclude=("plaid_item",))
    class Meta:
        additional=("id", "profile_id", "item_id", "request_id", "status", "timestamp")


class ReadProfileSchema(Schema):
    account: fields.Nested('ReadAccountSchema', exclude=("profile",))
    plaid_item: fields.Nested('ReadPlaidItemSchema', exclude=("profile",))

    class Meta:
        additional = ("id", "email", "first_name", "last_name", "is_demo_profile", "timestamp")


class ReadResetTokenSchema(Schema):
    profile = fields.Nested('ReadProfileSchema')

    class Meta:
        additional = ("id", "profile_id", "timestamp", "expiry")


class ReadHoldingSchema(Schema):
    account = fields.Nested('ReadAccountSchema', exclude=('holdings',))
    security = fields.Nested('ReadSecuritySchema', exclude=('holdings',))
    balances = fields.Nested('ReadHoldingBalanceSchema', many=True, exclude=("holdings",))

    class Meta:
        additional = ("id", "account_id", "security_id", "cost_basis", "quantity", "iso_currency_code", "timestamp")


class ReadSecuritySchema(Schema):
    class Meta:
        fields=("id", "profile_id", "account_id", "name", "ticker_symbol", "iso_currency_code", \
            "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp", \
            "sedol", "timestamp")


class ReadHoldingBalanceSchema(Schema):
    holding = fields.Nested('ReadHoldingSchema', exclude=('balances',))

    class Meta:
        additional = ("id", "holding_id", "cost_basis", "quantity", "timestamp")


class ReadAuthSchema(Schema):
    profile = fields.Nested('ReadProfileSchema',)

    class Meta:
        additional = ("token",)
