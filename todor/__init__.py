from flask import Flask
from .config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flasgger import Swagger
from todor.extensions import db, migrate
from .extensions import init_extensions
from .api.v1 import register_v1_blueprints

from todor.api.v1.auth_routes import bp as auth_bp
from todor.api.v1.event_routes import bp as event_bp
from todor.api.v1.attendee_routes import bp as attendee_bp
from todor.api.v1.session_routes import bp as session_bp
from todor.api.v1.user_routes import bp as user_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@localhost:5434/todoevents"
    )


    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(attendee_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(user_bp)

    init_extensions(app)
    register_v1_blueprints(app)

    app.config['SWAGGER'] = {
        'title': 'Todo Events API',
        'uiversion': 3
    }

    return app  