from marshmallow import Schema, fields


class CreateSecuritySchema(Schema):
    class Meta:
        fields = ("id", "profile_id", "account_id", "name", "ticker_symbol", "iso_currency_code",
                  "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp",
                  "sedol", "timestamp")


class ReadSecuritySchema(Schema):
    class Meta:
        fields = ("id", "profile_id", "account_id", "name", "ticker_symbol", "iso_currency_code",
                  "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp",
                  "sedol", "timestamp")


class UpdateSecuritySchema(Schema):
    class Meta:
        fields = ("id", "name", "ticker_symbol", "iso_currency_code",
                  "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp",
                  "sedol", "timestamp")


class ReadSecurityPriceSchema(Schema):
    class Meta:
        fields = ("id", "symbol", "high", "low", "open", "close", "volume",
                  "u_high", "u_low", "u_open", "u_close", "u_volume", "date", "change",
                  "change_percent", "change_over_time", "resolution", "timestamp")


class UpdateSecurityPriceSchema(Schema):
    class Meta:
        fields = ("id", "symbol", "high", "low", "open", "close", "volume",
                  "u_high", "u_low", "u_open", "u_close", "u_volume", "date", "change",
                  "change_percent", "change_over_time", "resolution")


class CreateSecurityPriceSchema(Schema):
    class Meta:
        fields = ("symbol", "high", "low", "open", "close", "volume",
                  "u_high", "u_low", "u_open", "u_close", "u_volume", "date", "change",
                  "change_percent", "change_over_time", "resolution")


class CreateIexBlacklistSchema(Schema):
    class Meta:
        fields = ("symbol",)


class ReadIexBlacklistSchema(Schema):
    class Meta:
        fields = ("id", "symbol", "timestamp")
