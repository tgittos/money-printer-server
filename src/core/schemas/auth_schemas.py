from marshmallow import Schema, fields


class ReadAuthSchema(Schema):
    profile = fields.Nested('ReadProfileSchema',)
    token = fields.Str()


class RegisterProfileSchema(Schema):
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class ResetPasswordSchema(Schema):
    email = fields.Str()
    token = fields.Str()
    password = fields.Str()


class LoginSchema(Schema):
    email = fields.Str()
    password = fields.Str()


class CreateResetTokenSchema(Schema):
    class Meta:
        fields = ("profile_id", "token", "expiry")


class ReadResetTokenSchema(Schema):
    profile = fields.Nested('ReadProfileSchema')

    class Meta:
        additional = ("id", "profile_id", "timestamp", "expiry")
