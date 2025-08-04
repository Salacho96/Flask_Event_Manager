import pytest

@pytest.fixture
def mock_user(mocker):
    """Fixture para crear un usuario simulado"""
    user = mocker.Mock()
    user.id = 1
    user.email = "test@example.com"
    user.role = "admin"
    return user


def test_get_users(client, mocker, mock_user):
    """Prueba GET /api/v1/users"""
    mock_query = mocker.patch("todor.models.user.User.query")
    mock_query.all.return_value = [mock_user]

    response = client.get("/api/v1/users/")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["id"] == 1
    assert data[0]["email"] == "test@example.com"
    assert data[0]["role"] == "admin"


def test_get_user(client, mocker, mock_user):
    """Prueba GET /api/v1/users/<id>"""
    mock_query = mocker.patch("todor.models.user.User.query")
    mock_query.get_or_404.return_value = mock_user

    response = client.get("/api/v1/users/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["email"] == "test@example.com"
    assert data["role"] == "admin"
