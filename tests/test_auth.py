import pytest
from flask import jsonify

@pytest.mark.parametrize(
    "existing_user, expected_status, expected_key, expected_message",
    [
        (True, 400, "error", "User already exists"),
        (False, 201, "message", "User registered successfully"),
    ]
)
def test_register_unit(client, mocker, existing_user, expected_status, expected_key, expected_message):
    """Prueba unitaria del endpoint de registro sin acceder a la BD."""

    
    mock_query = mocker.patch("todor.models.user.User.query")
    mock_query.filter_by.return_value.first.return_value = mocker.Mock() if existing_user else None

    
    mocker.patch("todor.models.user.User.hash_password", return_value="hashed123")

    mocker.patch("todor.extensions.db.session.add")
    mocker.patch("todor.extensions.db.session.commit")

    
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test1@test.com",
            "password": "123456",
            "role": "organizer"
        }
    )

    data = response.get_json()
    assert response.status_code == expected_status
    assert expected_message in data[expected_key]





class DummyRole(str):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj.value = value  
        return obj

def test_login_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.id = 1
    mock_user.email = "test@test.com"
    mock_user.role = DummyRole("ATTENDEE")
    mock_user.check_password.return_value = True

    
    mock_query = mocker.patch("todor.models.user.User.query")
    mock_query.filter_by.return_value.first.return_value = mock_user

    
    mocker.patch("todor.api.v1.auth_routes.create_access_token", return_value="fake-token")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@test.com", "password": "123456"}
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["access_token"] == "fake-token"
    assert data["user"]["role"] == "ATTENDEE"