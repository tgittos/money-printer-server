from marshmallow import Schema, fields

from core.models import Profile
from api.lib.globals import marshmallow_app as ma


class ReadProfileApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True

read_profile_schema = ReadProfileApiSchema()
read_profiles_schema = ReadProfileApiSchema(many=True)