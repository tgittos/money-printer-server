from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core.models import Security, SecurityPrice


class CreateSecuritySchema(Schema):
    class Meta:
        fields = ("name", "ticker_symbol", "iso_currency_code",
                  "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp",
                  "sedol", "timestamp")


class UpdateSecuritySchema(Schema):
    class Meta:
        fields = ("id", "name", "ticker_symbol", "iso_currency_code",
                  "institution_id", "institution_security_id", "security_id", "proxy_security_id", "cuisp",
                  "sedol", "timestamp")


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


class ReadSecurityPriceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SecurityPrice
        include_fk = True


class CreateIexBlacklistSchema(Schema):
    class Meta:
        fields = ("symbol",)


class RequestStockPriceSchema(Schema):
    class Meta:
        fields = ("symbol", "start", "end", "close_only")


class RequestStockPriceListSchema(Schema):
    class Meta:
        fields = ("symbols", "start", "end", "close_only")
