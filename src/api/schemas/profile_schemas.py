from marshmallow import Schema, fields

from core.models import Profile
from api.lib.globals import marshmallow_app as ma


class ReadProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True

read_profile_schema = ReadProfileSchema()
read_profiles_schema = ReadProfileSchema(many=True)