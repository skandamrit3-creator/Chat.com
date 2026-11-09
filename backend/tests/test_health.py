from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_serves_the_chrome_frontend() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Chat.com" in response.text


def test_health_reports_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_system_info_is_versioned() -> None:
    response = client.get("/api/v1/system")
    assert response.status_code == 200
    assert response.json()["version"] == "0.2.0"


def test_messages_can_be_saved_and_loaded() -> None:
    conversation_id = "automated-test-conversation"
    created = client.post(
        "/api/v1/messages",
        json={"conversation_id": conversation_id, "text": "Test message"},
    )
    assert created.status_code == 201
    assert created.json()["text"] == "Test message"
    assert created.json()["sender"] == "You"

    loaded = client.get(
        "/api/v1/messages",
        params={"conversation_id": conversation_id},
    )
    assert loaded.status_code == 200
    assert loaded.json()["messages"][-1]["text"] == "Test message"
