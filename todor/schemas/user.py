# app/schemas/user.py
from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserOutSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    role = fields.String()
