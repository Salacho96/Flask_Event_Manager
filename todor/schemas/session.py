from marshmallow import Schema, fields, validates_schema, ValidationError
from datetime import datetime

class SessionSchema(Schema):
    event_id = fields.Int(required=True)
    title = fields.Str(required=True)
    speaker = fields.Str(missing="")
    start_time = fields.Str(required=True)
    end_time = fields.Str(required=True)
    capacity = fields.Int(required=False, missing=0)

    @validates_schema
    def validate_times(self, data, **kwargs):
        try:
            start = datetime.fromisoformat(data["start_time"])
            end = datetime.fromisoformat(data["end_time"])
            if end <= start:
                raise ValidationError("End time must be after start time")
        except Exception:
            raise ValidationError("start_time and end_time must be in ISO format")
