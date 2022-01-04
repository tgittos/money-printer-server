from marshmallow import Schema, fields

from core.models import Account
from api.lib.globals import marshmallow_app as ma


class ReadAccountApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_fk = True

read_account_schema = ReadAccountApiSchema()
read_accounts_schema = ReadAccountApiSchema(many=True)