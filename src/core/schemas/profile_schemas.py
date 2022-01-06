from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core.models import Profile


class CreateProfileSchema(Schema):
    class Meta:
        fields = ("email", "password", "first_name", "last_name")


class ReadProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True


class UpdateProfileSchema(Schema):
    class Meta:
        fields = ("id", "first_name", "last_name")
