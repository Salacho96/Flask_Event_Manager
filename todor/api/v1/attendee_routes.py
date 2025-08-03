from flask import Blueprint, request, jsonify
from todor.extensions import db
from todor.models.attendee import Attendee
from todor.models.event import Event
from todor.models.user import User

bp = Blueprint("attendee", __name__, url_prefix="/api/v1/attendees")

@bp.route("/register", methods=["POST"])
def register_attendee():
    data = request.get_json()
    user_id = data.get("user_id")
    event_id = data.get("event_id")

    if not user_id or not event_id:
        return jsonify({"error": "user_id and event_id are required"}), 400

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
