from marshmallow import Schema, fields

class RegisterProfileSchema(Schema):
    username = fields.Email()
    first_name = fields.String()
    last_name = fields.String()

class AuthSchema(Schema):
    username = fields.Email()
    password = fields.Str()
