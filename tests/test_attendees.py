def test_register_attendee(client, auth_token):
    # Crear evento
    event_response = client.post(
        "/api/v1/events",
        json={
            "name": "Attendee Test Event",
            "description": "Event for attendees",
            "capacity": 10,
            "status": "draft",
            "start_at": "2025-08-10T09:00:00",
            "end_at": "2025-08-10T17:00:00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert event_response.status_code == 201
    event_id = event_response.get_json()["id"]

    # Registrar asistente con user_id requerido
    response = client.post(
        "/api/v1/attendees/register",
        json={"user_id": 4, "event_id": event_id},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Registered successfully"