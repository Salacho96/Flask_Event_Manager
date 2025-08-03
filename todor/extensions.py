# from flask import Blueprint

# bp = Blueprint('todo', __name__, url_prefix='/todo')

# @bp.route('/list')
# def index():
#     return "lista de eventos"

# @bp.route('/create')
# def create():
#     return "crear de eventos"

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask import jsonify
import bcrypt

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

