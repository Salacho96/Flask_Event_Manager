import pytest
from todor import create_app, db
from flask_jwt_extended import create_access_token
from todor.models.user import User

@pytest.fixture
def test_user(app):
    user = User(
        id=1,
        email="julian@test.com",
        role="admin",
        password_hash=User.hash_password("123456")
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def app():
    """Crea una instancia de la aplicación para pruebas."""
    app = create_app()

    # Configuración especial para testing
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret"
    })

    with app.app_context():
        db.create_all()  
        yield app
        # db.session.remove()
        # db.drop_all()  


@pytest.fixture
def client(app):
    """Cliente de prueba para realizar requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Runner para comandos CLI de Flask (si usas flask db, etc.)."""
    return app.test_cli_runner()


@pytest.fixture
def auth_token(app):
    """Genera un token JWT de prueba."""
    with app.app_context():
        return create_access_token(identity="1", additional_claims={"email": "test@test.com", "role": "organizer"})
