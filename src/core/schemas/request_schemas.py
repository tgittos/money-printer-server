from marshmallow import Schema, fields


class RequestAccountBalanceSchema(Schema):
    account = fields.Nested('ReadAccountSchema')

    class Meta:
        additional=("start", "end")

    
class RequestRegistrationSchema(Schema):
    class Meta:
        fields=("email", "first_name", "last_name")


class RequestPasswordResetSchema(Schema):
    profile = fields.Nested('ReadProfileSchema')

    class Meta:
        additional=("token", "password")


class RequestAuthSchema(Schema):
    class Meta:
        fields=("email", "password")
