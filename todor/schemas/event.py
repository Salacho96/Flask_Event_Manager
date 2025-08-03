# app/schemas/event.py
from marshmallow import Schema, fields, validate

class EventCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=3))
    description = fields.String()
    capacity = fields.Integer(required=True)
    status = fields.String(validate=validate.OneOf(["draft","published","cancelled"]))
    start_at = fields.DateTime(required=True)
    end_at = fields.DateTime(required=True)

class EventOutSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    capacity = fields.Int()
    registered = fields.Int()
    status = fields.String()
    start_at = fields.DateTime()
    end_at = fields.DateTime()

