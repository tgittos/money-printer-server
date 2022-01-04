from marshmallow import Schema, fields

from core.models import PlaidItem
from api.lib.globals import marshmallow_app as ma


class ReadPlaidItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaidItem
        include_fk = True

read_plaid_item_schema = ReadPlaidItemSchema()
read_plaid_items_schema = ReadPlaidItemSchema(many=True)