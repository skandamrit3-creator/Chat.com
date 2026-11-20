import hashlib
import hmac
import os
import re
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, LargeBinary, create_engine, desc, event, or_, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

ROOT = Path(__file__).resolve().parents[2]
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DATABASE_URL = os.getenv("DATABASE_URL")
if ENVIRONMENT == "production" and not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must point to persistent PostgreSQL in production.")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///" + str(ROOT / "chatcom-dev.db")
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

COOKIE_NAME = "chatcom_session"
SESSION_SECONDS = 60 * 60 * 24 * 30
PBKDF2_ROUNDS = 310_000
USERNAME_RE = re.compile(r"^[a-z0-9_]{3,24}$")
PASSWORD_MIN = 10
MESSAGE_MAX = 4000
IMAGE_MAX_BYTES = 5 * 1024 * 1024
IMAGE_TYPES = {"image/jpeg": b"\xff\xd8\xff", "image/png": b"\x89PNG\r\n\x1a\n", "image/gif": b"GIF8", "image/webp": b"RIFF"}


def build_engine(url: str):
    options = {"pool_pre_ping": True}
    if url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
    created = create_engine(url, **options)
    if url.startswith("sqlite"):
        @event.listens_for(created, "connect")
        def enable_foreign_keys(connection, _record):
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    return created


engine = build_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(24), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class LoginSession(Base):
    __tablename__ = "login_sessions"
    id = Column(Integer, primary_key=True)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at = Column(Integer, nullable=False)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    read_at = Column(DateTime(timezone=True), nullable=True)

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(32), nullable=False)
    size = Column(Integer, nullable=False)
    data = Column(LargeBinary, nullable=False)


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=24, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=PASSWORD_MIN, max_length=128)


class NewMessage(BaseModel):
    recipient: str = Field(min_length=3, max_length=24, pattern=r"^[A-Za-z0-9_]+$")
    body: str = Field(default="", max_length=MESSAGE_MAX)


app = FastAPI(title="Chat.com", version="1.0.0", docs_url=None, redoc_url=None, openapi_url=None)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def security_headers_and_origin(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH", "DELETE"} and request.url.path.startswith("/api/"):
        origin = request.headers.get("origin")
        host = request.headers.get("host", "").lower()
        if origin and urlsplit(origin).netloc.lower() != host:
            return JSONResponse({"detail": "Cross-origin request blocked."}, status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def normalize_username(value: str) -> str:
    username = value.strip().lower()
    if not USERNAME_RE.fullmatch(username):
        raise HTTPException(status_code=422, detail="Username must be 3–24 characters using letters, numbers, or underscores.")
    return username


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)
    return "pbkdf2_sha256$" + str(PBKDF2_ROUNDS) + "$" + salt.hex() + "$" + digest.hex()


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt_hex, digest_hex = encoded.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(rounds))
        return hmac.compare_digest(candidate.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def issue_session(user: User, response: Response, db: Session):
    token = secrets.token_urlsafe(32)
    db.add(LoginSession(token_hash=token_digest(token), user_id=user.id, expires_at=int(time.time()) + SESSION_SECONDS))
    db.commit()
    response.set_cookie(
        key=COOKIE_NAME, value=token, max_age=SESSION_SECONDS, httponly=True,
        secure=(ENVIRONMENT == "production"), samesite="lax", path="/",
    )


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Please sign in.")
    login = db.query(LoginSession).filter(
        LoginSession.token_hash == token_digest(token),
        LoginSession.expires_at > int(time.time()),
    ).first()
    if not login:
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")
    user = db.get(User, login.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Account not found.")
    return user


def iso_time(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def message_json(message: Message, current: User, peer: User, db=None):
    sender = current.username if message.sender_id == current.id else peer.username
    recipient = peer.username if message.recipient_id == peer.id else current.username
    attachment = db.query(Attachment).filter(Attachment.message_id == message.id).first() if db else None
    return {
        "id": message.id, "sender": sender, "recipient": recipient, "body": message.body,
        "created_at": iso_time(message.created_at), "read": message.read_at is not None,
        "image": ({"id": attachment.id, "filename": attachment.filename, "content_type": attachment.content_type, "size": attachment.size, "url": f"/api/attachments/{attachment.id}"} if attachment else None),
    }


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(ROOT / "index.html")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"service": "Chat.com", "status": "healthy"}


@app.post("/api/auth/register", status_code=201)
def register(data: Credentials, response: Response, db: Session = Depends(get_db)):
    username = normalize_username(data.username)
    user = User(username=username, password_hash=hash_password(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="That username is already registered.")
    db.refresh(user)
    issue_session(user, response, db)
    return {"user": {"id": user.id, "username": user.username}}


@app.post("/api/auth/login")
def login(data: Credentials, response: Response, db: Session = Depends(get_db)):
    username = normalize_username(data.username)
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    issue_session(user, response, db)
    return {"user": {"id": user.id, "username": user.username}}


@app.post("/api/auth/logout")
def logout(request: Request, response: Response, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        db.query(LoginSession).filter(LoginSession.token_hash == token_digest(token)).delete(synchronize_session=False)
        db.commit()
    response.delete_cookie(COOKIE_NAME, path="/", httponly=True, secure=(ENVIRONMENT == "production"), samesite="lax")
    return {"ok": True}


@app.get("/api/me")
def me(user: User = Depends(get_current_user)):
    return {"user": {"id": user.id, "username": user.username}}


@app.get("/api/users/search")
def search_users(q: str = Query(min_length=1, max_length=24), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    term = q.strip().lower()
    if not term:
        return {"users": []}
    users = db.query(User).filter(User.username.contains(term), User.id != user.id).order_by(User.username.asc()).limit(20).all()
    return {"users": [{"username": item.username} for item in users]}


@app.get("/api/conversations")
def conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Message).filter(
        or_(Message.sender_id == user.id, Message.recipient_id == user.id)
    ).order_by(desc(Message.id)).limit(500).all()
    peers = {}
    for item in rows:
        peer_id = item.recipient_id if item.sender_id == user.id else item.sender_id
        if peer_id not in peers:
            peer = db.get(User, peer_id)
            if peer:
                peers[peer_id] = {
                    "username": peer.username, "last_message": item.body,
                    "last_message_at": iso_time(item.created_at), "last_message_id": item.id, "unread": 0,
                }
        if item.recipient_id == user.id and item.read_at is None and peer_id in peers:
            peers[peer_id]["unread"] += 1
    result = sorted(peers.values(), key=lambda item: item["last_message_id"], reverse=True)
    return {"conversations": result}


@app.get("/api/messages/{username}")
def get_messages(
    username: str,
    after_id: int = Query(default=0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    peer_name = normalize_username(username)
    peer = db.query(User).filter(User.username == peer_name).first()
    if not peer:
        raise HTTPException(status_code=404, detail="User not found.")
    db.execute(update(Message).where(
        Message.sender_id == peer.id, Message.recipient_id == user.id, Message.read_at.is_(None),
    ).values(read_at=datetime.now(timezone.utc)))
    db.commit()
    query = db.query(Message).filter(or_(
        (Message.sender_id == user.id) & (Message.recipient_id == peer.id),
        (Message.sender_id == peer.id) & (Message.recipient_id == user.id),
    ))
    if after_id:
        rows = query.filter(Message.id > after_id).order_by(Message.id.asc()).limit(100).all()
    else:
        rows = list(reversed(query.order_by(desc(Message.id)).limit(100).all()))
    return {"messages": [message_json(item, user, peer, db) for item in rows]}


@app.post("/api/messages", status_code=201)
def send_message(data: NewMessage, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipient_name = normalize_username(data.recipient)
    body = data.body.strip()
    if not body:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")
    if len(body) > MESSAGE_MAX:
        raise HTTPException(status_code=422, detail="Message is too long.")
    if recipient_name == user.username:
        raise HTTPException(status_code=422, detail="You cannot message your own account.")
    recipient = db.query(User).filter(User.username == recipient_name).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="User not found.")
    message = Message(sender_id=user.id, recipient_id=recipient.id, body=body)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message": message_json(message, user, recipient, db)}

@app.post("/api/messages/image", status_code=201)
def send_image(recipient: str = Query(min_length=3, max_length=24), image: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipient_name = normalize_username(recipient)
    if recipient_name == user.username: raise HTTPException(status_code=422, detail="You cannot message your own account.")
    peer = db.query(User).filter(User.username == recipient_name).first()
    if not peer: raise HTTPException(status_code=404, detail="User not found.")
    if image.content_type not in IMAGE_TYPES: raise HTTPException(status_code=415, detail="Only JPEG, PNG, GIF, and WebP images are allowed.")
    data = image.file.read(IMAGE_MAX_BYTES + 1)
    if not data or len(data) > IMAGE_MAX_BYTES: raise HTTPException(status_code=413, detail="Image must be 5 MB or smaller.")
    if not data.startswith(IMAGE_TYPES[image.content_type]) or (image.content_type == "image/webp" and data[8:12] != b"WEBP"):
        raise HTTPException(status_code=415, detail="File content does not match the image type.")
    msg = Message(sender_id=user.id, recipient_id=peer.id, body="")
    db.add(msg); db.flush()
    name = re.sub(r"[^A-Za-z0-9._-]", "_", (image.filename or "image")[:255]) or "image"
    db.add(Attachment(message_id=msg.id, filename=name, content_type=image.content_type, size=len(data), data=data))
    db.commit(); db.refresh(msg)
    return {"message": message_json(msg, user, peer, db)}

@app.get("/api/attachments/{attachment_id}")
def get_attachment(attachment_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attachment = db.query(Attachment).join(Message, Attachment.message_id == Message.id).filter(Attachment.id == attachment_id, or_(Message.sender_id == user.id, Message.recipient_id == user.id)).first()
    if not attachment: raise HTTPException(status_code=404, detail="Image not found.")
    return Response(content=attachment.data, media_type=attachment.content_type, headers={"Content-Disposition": "inline; filename=\"image\"", "Cache-Control": "private, no-store"})
