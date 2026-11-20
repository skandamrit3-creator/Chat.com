# Chat.com

Chat.com is a deliberately small private messaging application with exactly two product capabilities:

1. Backend and accounts: registration, sign-in, session management, username search, and persistent message storage.
2. Private text chat: one-to-one text conversations between registered users.

There are no photos, attachments, voice/video calls, groups, channels, stories, feeds, bots, or AI features in this rebuild.

## Run locally

Requires Python 3.11 or newer.

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8060

Open http://127.0.0.1:8060. The local development database is SQLite at chatcom-dev.db.

Create two accounts in separate browser profiles (or one normal and one private window) to test messages between users.

## Production database and deployment

Production mode intentionally refuses to start without DATABASE_URL. Do not deploy with SQLite on an ephemeral application filesystem: it can lose user accounts and messages when the service is replaced.

For Render:
1. Create a managed PostgreSQL database.
2. Create a Python web service from this repository/branch.
3. Set ENVIRONMENT=production.
4. Set DATABASE_URL to the PostgreSQL internal connection string from that database.
5. Build command: pip install -r requirements.txt
6. Start command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
7. Health check path: /health

The database is not provisioned automatically by this repository, so no paid database is created without your approval.

## Included behavior

- Usernames are unique and case-insensitive; 3–24 letters, numbers, or underscores.
- Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, never plaintext.
- Login sessions are random, stored as SHA-256 token hashes, and delivered in HttpOnly cookies.
- Messages are stored in PostgreSQL in production and SQLite during local development.
- A user can only retrieve messages exchanged between their own account and the selected recipient.
- Text messages are limited to 4,000 characters.
- The browser refreshes conversations and the active chat automatically.
- The frontend is served by the same FastAPI service as the API, avoiding separate frontend/API origin configuration.

## Tests

    pytest -q
