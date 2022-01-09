from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

from core.models import Account
from api.flask_app import ma

class ReadAccountApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_fk = True

read_account_schema = ReadAccountApiSchema()
read_accounts_schema = ReadAccountApiSchema(many=True)