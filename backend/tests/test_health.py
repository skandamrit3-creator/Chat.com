from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_reports_service_online() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Chat.com API"


def test_health_reports_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_system_info_is_versioned() -> None:
    response = client.get("/api/v1/system")
    assert response.status_code == 200
    assert response.json()["version"] == "0.1.0"
