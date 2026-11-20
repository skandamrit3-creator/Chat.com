from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app import main


def make_client(monkeypatch):
    test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    test_sessions = sessionmaker(bind=test_engine, autoflush=False, autocommit=False, expire_on_commit=False)
    monkeypatch.setattr(main, "engine", test_engine)
    monkeypatch.setattr(main, "SessionLocal", test_sessions)
    return TestClient(main.app), test_engine


def test_accounts_search_and_private_text_chat(monkeypatch):
    alice, engine = make_client(monkeypatch)
    with alice:
        assert alice.get("/health").json()["status"] == "healthy"
        created = alice.post("/api/auth/register", json={"username": "Alice_01", "password": "correct-horse-123"})
        assert created.status_code == 201
        assert created.json()["user"]["username"] == "alice_01"
        bob = TestClient(main.app)
        with bob:
            assert bob.post("/api/auth/register", json={"username": "bob_02", "password": "another-safe-456"}).status_code == 201
            search = alice.get("/api/users/search?q=bob")
            assert [item["username"] for item in search.json()["users"]] == ["bob_02"]
            sent = alice.post("/api/messages", json={"recipient": "bob_02", "body": "Hello Bob"})
            assert sent.status_code == 201
            inbox = bob.get("/api/messages/alice_01")
            assert [item["body"] for item in inbox.json()["messages"]] == ["Hello Bob"]
            assert inbox.json()["messages"][0]["sender"] == "alice_01"
            assert bob.post("/api/messages", json={"recipient": "alice_01", "body": "Hello Alice"}).status_code == 201
            history = alice.get("/api/messages/bob_02")
            assert [item["body"] for item in history.json()["messages"]] == ["Hello Bob", "Hello Alice"]
            stranger = TestClient(main.app)
            with stranger:
                assert stranger.post("/api/auth/register", json={"username": "stranger", "password": "stranger-pass-789"}).status_code == 201
                private = stranger.get("/api/messages/alice_01")
                assert all("Hello" not in item["body"] for item in private.json()["messages"])
            assert alice.get("/api/conversations").json()["conversations"][0]["username"] == "bob_02"
            assert bob.post("/api/auth/logout").status_code == 200
            assert bob.get("/api/me").status_code == 401
    main.Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_rejects_short_password(monkeypatch):
    client, engine = make_client(monkeypatch)
    with client:
        response = client.post("/api/auth/register", json={"username": "user_01", "password": "short"})
        assert response.status_code == 422
    main.Base.metadata.drop_all(bind=engine)
    engine.dispose()
