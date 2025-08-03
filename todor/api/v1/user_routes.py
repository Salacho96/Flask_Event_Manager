from flask import Blueprint, jsonify
from todor.models.user import User

bp = Blueprint("user", __name__, url_prefix="/api/v1/users")

@bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "role": u.role} for u in users])

@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "email": user.email, "role": user.role})
