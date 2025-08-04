import pytest
from datetime import datetime
import jwt

@pytest.fixture
def mock_event(
    mocker):
    """Crea un evento simulado para las pruebas."""
    mock_event = mocker.Mock()
    mock_event.id = 1
    mock_event.name = "Sample Event"
    mock_event.capacity = 100
    mock_event.status = "DRAFT" 
    return mock_event


def test_get_events(client, mocker, mock_event):
    mock_query = mocker.patch("todor.models.event.Event.query")
    mock_query.filter.return_value.all.return_value = [mock_event]
    mock_query.all.return_value = [mock_event]

    response = client.get("/api/v1/events")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["name"] == "Sample Event"
    assert data[0]["capacity"] == 100


def test_create_event_success(client, mocker, mock_event):
    """Prueba unitaria de POST /api/v1/events (creación exitosa)"""
    
    mock_jwt = mocker.patch("todor.api.v1.event_routes.jwt")
    mock_jwt.decode.return_value = {"sub": "1"}

    
    mock_schema = mocker.patch("todor.api.v1.event_routes.EventCreateSchema")
    mock_schema.return_value.load.return_value = {
        "name": "New Event",
        "description": "Test event",
        "capacity": 50,
        "status": "draft",
        "start_at": datetime.now(),
        "end_at": datetime.now(),
    }

    
    mocker.patch("todor.models.event.Event", return_value=mock_event)

    
    mocker.patch("todor.extensions.db.session.add")
    mocker.patch("todor.extensions.db.session.commit")

    response = client.post(
        "/api/v1/events",
        json={"name": "New Event", "capacity": 50},
        headers={"Authorization": "Bearer fake-token"},
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "Event created"


def test_create_event_invalid_token(client, mocker):
    """Prueba POST /api/v1/events con token inválido"""
    mock_decode = mocker.patch("todor.api.v1.event_routes.jwt.decode")
    mock_decode.side_effect = jwt.InvalidTokenError("Invalid token")

    response = client.post(
        "/api/v1/events",
        json={"name": "New Event", "capacity": 50},
        headers={"Authorization": "Bearer bad-token"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid token"


def test_update_event_success(client, mocker, mock_event):
    """Prueba PUT /api/v1/events/<id>"""
    mock_query = mocker.patch("todor.models.event.Event.query")
    mock_query.get_or_404.return_value = mock_event

    mocker.patch("todor.extensions.db.session.commit")

    response = client.put(
        "/api/v1/events/1",
        json={"name": "Updated Event", "capacity": 200}
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Event updated"
    assert mock_event.name == "Updated Event"
    assert mock_event.capacity == 200


def test_delete_event_success(client, mocker, mock_event):
    """Prueba DELETE /api/v1/events/<id>"""
    mock_query = mocker.patch("todor.models.event.Event.query")
    mock_query.get_or_404.return_value = mock_event

    mocker.patch("todor.extensions.db.session.delete")
    mocker.patch("todor.extensions.db.session.commit")

    response = client.delete("/api/v1/events/1")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Event deleted"
