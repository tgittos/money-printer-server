from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from stonk_server.models import Security, SecurityPrice, IexBlacklist
from stonk_server.app import ma


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

class ReadSecurityApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Security
        include_fk = True


class ReadSecurityPriceApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SecurityPrice
        include_fk = True


class ReadIexBlacklistApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IexBlacklist
        include_fk = True

read_security_schema = ReadSecurityApiSchema()
read_securities_schema = ReadSecurityApiSchema(many=True)

read_security_price_schema = ReadSecurityPriceApiSchema()
read_security_prices_schema = ReadSecurityPriceApiSchema(many=True)

read_iex_blacklist_schema = ReadIexBlacklistApiSchema()
read_iex_blacklists_schema = ReadIexBlacklistApiSchema(many=True)