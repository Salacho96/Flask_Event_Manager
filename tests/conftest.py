import pytest
from flask import Flask
from todor.extensions import db
from todor.api.v1.auth_routes import bp as auth_bp
from todor.api.v1.event_routes import bp as event_bp
from todor.api.v1.session_routes import bp as session_bp
from todor.api.v1.user_routes import bp as user_bp

@pytest.fixture(scope='module')
def app():
    """Fixture para la aplicación Flask con contexto de prueba."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    
    db.init_app(app)

    
    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(user_bp)
    
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """Fixture para el cliente de pruebas HTTP."""
    return app.test_client()
