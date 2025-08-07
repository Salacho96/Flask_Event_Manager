from flask import Blueprint, request, jsonify
from todor.extensions import db
from todor.models.attendee import Attendee
from todor.models.event import Event
from todor.models.user import User
from todor.schemas.attendee import AttendeeRegisterSchema
from marshmallow import ValidationError


bp = Blueprint("attendee", __name__, url_prefix="/api/v1/attendees")
attendee_schema = AttendeeRegisterSchema()

@bp.route("/register", methods=["POST"])
def register_attendee():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        data = attendee_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = data["user_id"]
    event_id = data["event_id"]

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if len(event.attendances) >= event.capacity:
        return jsonify({"error": "Event is full"}), 400

    attendee = Attendee(user_id=user_id, event_id=event_id)
    db.session.add(attendee)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@bp.route("/<int:user_id>", methods=["GET"])
def get_user_events(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([{"event_id": a.event_id, "event_name": a.event.name} for a in user.attendances])
