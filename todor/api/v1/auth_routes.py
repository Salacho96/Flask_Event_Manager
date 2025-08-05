from flask import Blueprint, request, jsonify
from todor.extensions import db
from todor.models.user import User, RoleEnum
from flask_jwt_extended import create_access_token
from datetime import timedelta


bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    
    role_value = data.get("role", "ATTENDEE").upper()

    if role_value not in RoleEnum.__members__:
        return jsonify({
            "error": f"Invalid role. Must be one of: {', '.join(RoleEnum.__members__.keys())}"
        }), 400

    new_user = User(
        email=data["email"],
        password_hash=User.hash_password(data["password"]),
        role=RoleEnum[role_value]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "email": new_user.email,
            "role": new_user.role.value
        }
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "email": user.email,
            "role": user.role.value
        },
        expires_delta=timedelta(hours=24)  
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }), 200
