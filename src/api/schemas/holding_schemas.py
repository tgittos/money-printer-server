from marshmallow import Schema, fields

from core.models import Holding
from api.lib.globals import marshmallow_app as ma


class ReadHoldingApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Holding
        include_fk = True

read_holding_schema = ReadHoldingApiSchema()
read_holdings_schema = ReadHoldingApiSchema(many=True)