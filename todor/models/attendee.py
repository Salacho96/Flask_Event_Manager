# app/models/attendee.py
from todor.extensions import db
from datetime import datetime

class Attendee(db.Model):
    __tablename__ = "attendee"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="attendances")
    event = db.relationship("Event", backref="attendances")
    session = db.relationship("Session", backref="attendances")
