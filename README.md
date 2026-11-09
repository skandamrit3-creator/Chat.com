# Chat.com

**Chat.com** is an Android-first, privacy-focused messaging platform designed for reliable real-time communication, with a future integration path to COSMIC AI.

## Project status

This repository is at the foundation stage. The first milestone is a runnable development skeleton with:
- A Flutter Android client.
- A FastAPI backend with health and version endpoints.
- PostgreSQL-ready configuration and SQLAlchemy models.
- A WebSocket entry point for real-time messaging.
- Automated backend tests and GitHub Actions checks.

No production authentication, message delivery, encryption, calls, or cloud storage is claimed until those systems are implemented and tested.

## Architecture

| Layer | Technology | Responsibility |
|---|---|---|
| Android client | Flutter / Dart | UI, local state, secure client storage |
| API | FastAPI / Python | Authentication, profiles, chat APIs |
| Realtime | WebSockets | Live message and presence events |
| Database | PostgreSQL | Users, devices, conversations, messages |
| Cache / jobs | Redis (later phase) | Presence, rate limits, background work |
| Media | Private object storage (later phase) | Images, video, documents, voice notes |
| Push | Firebase Cloud Messaging (later phase) | Offline notifications |

## Repository layout

```
app/                 Flutter application
backend/             FastAPI service and tests
docs/                Architecture and security decisions
.github/workflows/   CI automation
```

## Quick start

### Backend

Requirements: Python 3.11+

```bash
cd backend
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8059
```

Health check: `http://127.0.0.1:8059/health`

Run tests:

```bash
pytest
```

### Android app

Install Flutter and Android SDK, then:

```bash
cd app
flutter pub get
flutter run
```

## Configuration and security

- Copy `backend/.env.example` to `backend/.env` for local development.
- Never commit API keys, OTP secrets, signing keys, database passwords, or private encryption keys.
- The development configuration is not production-hardened.
- End-to-end encryption must be designed and independently reviewed before being advertised as enabled.
- User-uploaded media must use private object storage and short-lived authorized access; personal Google Drive storage is not an application backend.

## Development principles

1. Build in small, testable milestones.
2. Keep secrets out of source control.
3. Use database migrations for schema changes.
4. Treat delivery states honestly (sent, delivered, read).
5. Design security and privacy into the data model from the beginning.
6. Do not ship placeholder functionality as if it were production-ready.

## Roadmap

1. Foundation and CI.
2. Phone-number authentication and device sessions.
3. One-to-one messaging, persistence, and offline sync.
4. Group messaging and media.
5. Audited end-to-end encryption and encrypted backups.
6. Voice/video calls, communities, channels, and status.
7. AI assistance and optional COSMIC AI integration.
8. Android release, signing, updates, monitoring, and deployment.

## License

All rights reserved unless a license is added by the project owner.
