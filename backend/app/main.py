import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Chat.com local development preview API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_FILE = ROOT_DIR / "index.html"
DATABASE_FILE = Path(__file__).resolve().parents[1] / "data" / "chat_com_preview.db"


class MessageCreate(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=4000)


def get_connection() -> sqlite3.Connection:
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS preview_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        existing = connection.execute(
            "SELECT COUNT(*) FROM preview_messages WHERE conversation_id = ?",
            ("general",),
        ).fetchone()[0]
        if existing == 0:
            connection.execute(
                """
                INSERT INTO preview_messages
                    (conversation_id, sender, text, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    "general",
                    "Chat.com",
                    "Welcome to your Chat.com development preview. Messages you send here are saved by the local backend.",
                    datetime.now(timezone.utc).isoformat(),
                ),
            )


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    if not FRONTEND_FILE.is_file():
        raise HTTPException(status_code=404, detail="Frontend index.html is missing")
    return FileResponse(FRONTEND_FILE, media_type="text/html")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "chat-com-api", "version": "0.2.0"}


@app.get(f"{settings.api_prefix}/system", tags=["system"])
def system_info() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": "0.2.0",
        "environment": settings.app_env,
        "frontend": "/",
        "database": "sqlite-local-preview",
    }


@app.get(f"{settings.api_prefix}/messages", tags=["messages"])
def list_messages(
    conversation_id: str = Query(default="general", min_length=1, max_length=100),
) -> dict[str, list[dict[str, object]]]:
    initialize_database()
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, sender, text, created_at
            FROM preview_messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            LIMIT 200
            """,
            (conversation_id,),
        ).fetchall()
    return {"messages": [dict(row) for row in rows]}


@app.post(f"{settings.api_prefix}/messages", tags=["messages"], status_code=201)
def create_message(payload: MessageCreate) -> dict[str, object]:
    initialize_database()
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO preview_messages
                (conversation_id, sender, text, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (payload.conversation_id, "You", payload.text.strip(), created_at),
        )
        message_id = cursor.lastrowid
    return {
        "id": message_id,
        "conversation_id": payload.conversation_id,
        "sender": "You",
        "text": payload.text.strip(),
        "created_at": created_at,
    }
