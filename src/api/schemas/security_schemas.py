from marshmallow import Schema, fields

from core.models import Security, SecurityPrice, IexBlacklist
from api.app import ma


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