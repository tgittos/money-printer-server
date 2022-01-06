from marshmallow import Schema, fields

from core.models import ResetToken


class ReadAuthSchema(Schema):
    profile = fields.Nested('ReadProfileSchema',)
    token = fields.Str()


class RegisterProfileSchema(Schema):
    email = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class ResetPasswordSchema(Schema):
    email = fields.Str(required=True)
    token = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class CreateResetTokenSchema(Schema):
    class Meta:
        fields = ("profile_id", "token", "expiry")


class ReadResetTokenSchema(Schema):

    class Meta:
        model = ResetToken
