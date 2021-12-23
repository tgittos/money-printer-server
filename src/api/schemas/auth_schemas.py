from marshmallow import Schema, fields

class RegisterProfileSchema(Schema):
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()

class AuthSchema(Schema):
    email = fields.Email()
    password = fields.Str()
