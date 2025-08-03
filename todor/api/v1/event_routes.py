from flask import Blueprint, request, jsonify
from todor.extensions import db
from todor.models.event import Event, EventStatus
# from datetime import datetime   
# from flask_jwt_extended import get_jwt, jwt_required
from todor.schemas.event import EventCreateSchema
from marshmallow import ValidationError
import jwt
from flask import current_app



bp = Blueprint("event", __name__, url_prefix="/api/v1/events")

@bp.route("", methods=["GET"])
def get_events():
    search = request.args.get("search", "")
    query = Event.query
    if search:
        query = query.filter(Event.name.ilike(f"%{search}%"))
    events = query.all()
    return jsonify([{"id": e.id, "name": e.name, "capacity": e.capacity, "status": e.status} for e in events])



@bp.route("", methods=["POST"])
def create_event():
    data = request.get_json()
    auth_header = request.headers.get("Authorization")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    print(f"JWT Token: {token}")

    # Decodificar el token JWT
    try:
        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        print("Decoded token:", decoded_token)
        created_by_id = int(decoded_token["sub"])  # Usuario que crea el evento
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    # Validar datos del body con Marshmallow
    try:
        validated_data = EventCreateSchema().load(data)
    except ValidationError as err:
        print("Validation errors:", err.messages)
        return jsonify({"errors": err.messages}), 422

    # Validar el status
    status_value = validated_data.get("status", "draft").upper()
    if status_value not in EventStatus.__members__:
        return jsonify({
            "error": f"Invalid status. Must be one of: {', '.join(EventStatus.__members__.keys())}"
        }), 400

    event = Event(
        name=validated_data["name"],
        description=validated_data.get("description"),
        capacity=validated_data["capacity"],
        status=EventStatus[status_value],
        start_at=validated_data["start_at"],
        end_at=validated_data["end_at"],
        created_by_id=created_by_id
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event created", "id": event.id}), 201


@bp.route("/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    event.name = data.get("name", event.name)
    event.description = data.get("description", event.description)
    event.capacity = data.get("capacity", event.capacity)

    if "status" in data:
        status_value = data["status"].upper()
        if status_value in EventStatus.__members__:
            event.status = EventStatus[status_value] 
        else:
            return jsonify({
                "error": f"Invalid status. Must be one of: {', '.join(EventStatus.__members__.keys())}"
            }), 400
        
    db.session.commit()
    
    return jsonify({"message": "Event updated"})


@bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})
