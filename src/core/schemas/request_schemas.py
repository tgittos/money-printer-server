from marshmallow import Schema, fields


class RequestAccountBalanceSchema(Schema):
    account = fields.Nested('ReadAccountSchema')

    class Meta:
        additional=("start", "end")

    
class RequestRegistrationSchema(Schema):
    class Meta:
        fields=("email", "first_name", "last_name")


class RequestPasswordResetSchema(Schema):
    email = fields.Str()
    token = fields.Str()
    password = fields.Str()


class RequestAuthSchema(Schema):
    email = fields.Str()
    password = fields.Str()
