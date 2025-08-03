def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "123456",
        "role": "organizer"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"


def test_login_user(client):
    # Primero registrar usuario
    client.post("/api/v1/auth/register", json={
        "email": "login@test.com",
        "password": "123456",
        "role": "attendee"
    })

    # Ahora login
    response = client.post("/api/v1/auth/login", json={
        "email": "login@test.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
