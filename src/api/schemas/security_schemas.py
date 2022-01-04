from marshmallow import Schema, fields

from core.models import Security, SecurityPrice, IexBlacklist
from api.lib.globals import marshmallow_app as ma


class ReadSecuritySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Security
        include_fk = True


class ReadSecurityPriceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SecurityPrice
        include_fk = True


class ReadIexBlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IexBlacklist
        include_fk = True

read_security_schema = ReadSecuritySchema()
read_securities_schema = ReadSecuritySchema(many=True)

read_security_price_schema = ReadSecurityPriceSchema()
read_security_prices_schema = ReadSecurityPriceSchema(many=True)

read_iex_blacklist_schema = ReadIexBlacklistSchema()
read_iex_blacklists_schema = ReadIexBlacklistSchema(many=True)