# app/models/event.py
from todor.extensions import db
from datetime import datetime
from enum import Enum

class EventStatus(str, Enum):
    DRAFT = "DREAFT"
    PUBLISHED = "PUBLISHED"
    CANCELLED = "CANCELLED"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=True, index=True)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, nullable=True)
    registered = db.Column(db.Integer, default=0)  # para cachear conteo
    status = db.Column(db.Enum(EventStatus), default=EventStatus.DRAFT, nullable=True)
    start_at = db.Column(db.DateTime, nullable=True)
    end_at = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_by = db.relationship("User", backref="created_events")
    created_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=True)
    sessions = db.relationship("Session", backref="event", cascade="all, delete-orphan")
