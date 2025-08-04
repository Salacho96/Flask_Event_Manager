import pytest
from datetime import datetime

@pytest.fixture
def mock_session(mocker):
    """Crea una sesión simulada para las pruebas."""
    mock_session = mocker.Mock()
    mock_session.id = 1
    mock_session.title = "Sample Session"
    mock_session.start_time = datetime.now().isoformat()
    mock_session.end_time = datetime.now().isoformat()
    return mock_session


def test_get_sessions(client, mocker, mock_session):
    """Prueba GET /api/v1/sessions/<event_id>"""
    mock_query = mocker.patch("todor.models.session.Session.query")
    mock_query.filter_by.return_value.all.return_value = [mock_session]

    response = client.get("/api/v1/sessions/1")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["title"] == "Sample Session"


def test_create_session_success(client, mocker, mock_session):
    """Prueba POST /api/v1/sessions (creación exitosa)"""
    
    mock_event = mocker.patch("todor.models.event.Event.query")
    mock_event.get.return_value = True

    mocker.patch("todor.models.session.Session", return_value=mock_session)
    mocker.patch("todor.extensions.db.session.add")
    mocker.patch("todor.extensions.db.session.commit")

    response = client.post(
        "/api/v1/sessions",
        json={
            "event_id": 1,
            "title": "New Session",
            "start_time": "2025-08-01T09:00:00",
            "end_time": "2025-08-01T14:00:00"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "Session created"
