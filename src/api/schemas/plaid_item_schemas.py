from marshmallow import Schema, fields

from core.models import PlaidItem
from api.flask_app import ma


class ReadPlaidItemApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaidItem
        include_fk = True

read_plaid_item_schema = ReadPlaidItemApiSchema()
read_plaid_items_schema = ReadPlaidItemApiSchema(many=True)