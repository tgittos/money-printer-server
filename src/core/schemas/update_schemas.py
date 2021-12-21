from marshmallow import Schema, fields


class UpdateScheduledJobSchema(Schema):
    class Meta:
        fields = ("id", "cron", "job_name", "json_args", "queue", "active")


class UpdateAccountBalanceSchema(Schema):
    class Meta:
        fields = ("id", "available", "current")


class UpdateAccountSchema(Schema):
    class Meta:
        fields = ("id", "account_id", "name", "official_name", "type", "subtype")


class UpdateHoldingBalanceSchema(Schema):
    class Meta:
        fields = ("id", "cost_basis", "quantity")
    

class UpdateHoldingSchema(Schema):
    class Meta:
        fields = ("id", "cost_basis", "quantity", "iso_currency_code")


class UpdateInvestmentTransactionSchema(Schema):
    class Meta:
        fields = ("id", "name", "amount", "feeds", "price", "quantity", "date",\
            "investment_transaction_id", "iso_currency_code", "type", "subtype")


class UpdatePlaidItemSchema(Schema):
    class Meta:
        fields = ("id", "status")
    

class UpdateProfileSchema(Schema):
    class Meta:
        fields = ("id", "first_name", "last_name")


class UpdateSecurityPriceSchema(Schema):
    class Meta:
        fields = ("id", "symbol", "high", "low", "open", "close", "volume", \
            "u_high", "u_low", "u_open", "u_close", "u_volume", "date", "change", \
            "change_percent", "change_over_time", "resolution")
        

class UpdateSecuritySchema(Schema):
    class Meta:
        fields=("id", "name", "ticker_symbol", "iso_currency_code", \
            "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp", \
            "sedol", "timestamp")