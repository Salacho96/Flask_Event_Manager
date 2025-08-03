from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta


def test_create_event(client):
    payload = {
        "sub": "1",  
        "email": "test@example.com",
        "role": "organizer",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    response = client.post(
        "/api/v1/events",
        json={
            "name": "Test Event",
            "description": "Test description",
            "capacity": 50,
            "status": "draft",
            "start_at": "2025-08-10T09:00:00",
            "end_at": "2025-08-10T17:00:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # 3. Verificaciones
    print(response.get_json())  # Debug: Ver respuesta completa
    assert response.status_code == 201
    assert "id" in response.get_json()




def test_get_events(client, auth_token):
    response = client.get("/api/v1/events", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
