from flask import Blueprint, request, jsonify
from todor.extensions import db
from todor.models.session import Session
from todor.models.event import Event
from todor.schemas.session import SessionSchema

bp = Blueprint("session", __name__, url_prefix="/api/v1/sessions")
session_schema = SessionSchema()

@bp.route("", methods=["POST"])
def create_session():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    # ✅ Validación con Marshmallow
    try:
        data = session_schema.load(json_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    event = Event.query.get(data["event_id"])
    if not event:
        return jsonify({"error": "Event not found"}), 404

    from datetime import datetime
    start_at = datetime.fromisoformat(data["start_time"])
    end_at = datetime.fromisoformat(data["end_time"])

    session = Session(
        event_id=data["event_id"],
        title=data["title"],
        speaker=data.get("speaker", ""),
        start_at=start_at,
        end_at=end_at,
        capacity=data.get("capacity", 0)
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
