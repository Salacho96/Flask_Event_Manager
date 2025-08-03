from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta

def test_create_session(client):
    payload = {
        "sub": "1",  
        "email": "test@example.com",
        "role": "organizer",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    
    event_response = client.post(
        "/api/v1/events",
        json={
            "name": "Session Test Event",
            "description": "Event for sessions",
            "capacity": 50,
            "status": "draft",
            "start_at": "2025-08-10T09:00:00",
            "end_at": "2025-08-10T17:00:00",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert event_response.status_code == 201
    event_id = event_response.get_json()["id"]

    # Crear sesión
    session_response = client.post(
        "/api/v1/sessions",
        json={
            "event_id": event_id,
            "title": "AI and Cloud",
            "speaker": "DR. COOPER",
            "capacity": 2,
            "start_time": "2025-08-01T09:00:00",
            "end_time": "2025-08-01T14:00:00",
            "created_at": "2025-08-01T09:00:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert session_response.status_code == 201
    session_data = session_response.get_json()
    assert "id" in session_data
    assert session_data["message"] == "Session created"

