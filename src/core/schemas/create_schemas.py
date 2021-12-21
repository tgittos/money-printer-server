from marshmallow import Schema, fields

class CreateScheduledJobSchema(Schema):
    class Meta:
        fields = ("cron", "job_name", "json_args", "queue", "active")


class CreateJobResultSchema(Schema):
    class Meta:
        fields = ("job_id", "success", "log", "queue")


class CreateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("account_id", "available", "current", "iso_currency_code")


class CreateAccountSchema(Schema):
    class Meta:
        fields = ("plaid_item_id", "profile_id", "account_id", \
            "name", "official_name", "type", "subtype")


class CreateHoldingBalanceSchema(Schema):
    class Meta:
        fields = ("holding_id", "cost_basis", "quantity")


class CreateHoldingSchema(Schema):
    class Meta:
        fields = ("account_id", "security_id", "cost_basis", "quantity", "iso_currency_code")


class CreateIexBlacklistSchema(Schema):
    class Meta:
        fields = ("symbol",)


class CreateInvestmentTransactionSchema(Schema):
    class Meta:
        fields = ("account_id", "name", "amount", "feeds", "price", "quantity", "date",\
            "investment_transaction_id", "iso_currency_code", "type", "subtype")


class CreatePlaidItemSchema(Schema):
    class Meta:
        fields = ("profile_id", "item_id", "access_token", "request_id", "status")


class CreateProfileSchema(Schema):
    class Meta:
        fields = ("email", "password", "first_name", "last_name")


class CreateResetTokenSchema(Schema):
    class Meta:
        fields = ("profile_id", "token", "expiry")
    

class CreateSecurityPriceSchema(Schema):
    class Meta:
        fields = ("symbol", "high", "low", "open", "close", "volume", \
            "u_high", "u_low", "u_open", "u_close", "u_volume", "date", "change", \
            "change_percent", "change_over_time", "resolution")


class CreateSecuritySchema(Schema):
    class Meta:
        fields=("id", "profile_id", "account_id", "name", "ticker_symbol", "iso_currency_code", \
            "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp", \
            "sedol", "timestamp")

class CreateInstantJobSchema(Schema):
    class Meta:
        fields=("job_name", "json_args")
