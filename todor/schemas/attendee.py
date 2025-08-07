from marshmallow import Schema, fields

class AttendeeRegisterSchema(Schema):
    user_id = fields.Int(required=True)
    event_id = fields.Int(required=True)