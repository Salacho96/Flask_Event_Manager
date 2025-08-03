from flask import Blueprint, request, jsonify
from todor.extensions import db
from todor.models.session import Session
from todor.models.event import Event

bp = Blueprint("session", __name__, url_prefix="/api/v1/sessions")

@bp.route("", methods=["POST"])
def create_session():
    data = request.get_json()
    event_id = data.get("event_id")
    title = data.get("title")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not event_id or not title or not start_time or not end_time:
        return jsonify({"error": "All fields are required"}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    from datetime import datetime
    start_at = datetime.fromisoformat(start_time)
    end_at = datetime.fromisoformat(end_time)

    if end_time <= start_time:
        return jsonify({"error": "End time must be after start time"}), 400

    session = Session(
        event_id=event_id,
        title=title,
        start_at=start_at,
        end_at=end_at,
        capacity=data.get("capacity", 0),
        speaker=data.get("speaker", "")
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({"message": "Session created", "id": session.id}), 201

@bp.route("/<int:event_id>", methods=["GET"])
def get_sessions(event_id):
    sessions = Session.query.filter_by(event_id=event_id).all()
    return jsonify([{
        "id": s.id,
        "title": s.title,
        "start_time": s.start_time,
        "end_time": s.end_time
    } for s in sessions])
