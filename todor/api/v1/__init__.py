from flask import Blueprint
from .auth_routes import bp as auth_bp
from .event_routes import bp as events_bp
from .session_routes import bp as sessions_bp
from .attendee_routes import bp as attendees_bp
from .user_routes import bp as users_bp

def register_v1_blueprints(app):
    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    api_v1.register_blueprint(auth_bp)
    api_v1.register_blueprint(events_bp)
    api_v1.register_blueprint(sessions_bp)
    api_v1.register_blueprint(attendees_bp)
    api_v1.register_blueprint(users_bp)
    app.register_blueprint(api_v1)
