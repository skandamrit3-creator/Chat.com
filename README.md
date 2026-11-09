# Chat.com

**Chat.com** is an Android-first, privacy-focused messaging app built for fast, dependable communication. It is a separate product from COSMIC AI, with an optional secure integration path in the future.

## Product plan

The complete product map, screen behavior, visual direction, security rules, repository structure, and review agreement are documented here:

- [Product mind map](docs/MIND_MAP.md)
- [Product specification](docs/PRODUCT_SPEC.md)
- [UI guidelines](docs/UI_GUIDELINES.md)
- [Repository file plan](docs/FILE_STRUCTURE.md)
- [Security baseline](docs/SECURITY_BASELINE.md)
- [Architecture decisions](docs/ARCHITECTURE.md)
- [User review process](docs/REVIEW_PROCESS.md)

## Current implementation

- Flutter / Dart Android client starter.
- FastAPI backend with root, health, and system information endpoints.
- Development configuration and backend tests.
- GitHub Actions workflow for backend checks.

This is an early foundation. Real phone OTP, user accounts, persisted messaging, end-to-end encryption, calls, media transfer, and production deployment are not yet implemented. A configured CI workflow is not proof of a passing run; check the Actions tab for actual results.

## Architecture

| Layer | Technology | Responsibility |
|---|---|---|
| Android client | Flutter / Dart | UI, navigation, local state, secure device storage |
| API | FastAPI / Python | Identity, profiles, conversations, authorization |
| Realtime | WebSockets | Live events and message delivery |
| Database | PostgreSQL | Users, devices, conversations, messages |
| Cache / jobs | Redis | Presence, rate limits, background tasks |
| Media | Private object storage | Photos, videos, documents, voice notes |
| Push | Firebase Cloud Messaging | Offline notifications |

## Local development

### Backend

Python 3.11+:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8059
```

Health check: `http://127.0.0.1:8059/health`

Run tests from the backend directory:

```bash
pytest
```

### Android app

Install Flutter and the Android SDK:

```bash
cd app
flutter pub get
flutter run
```

## Development agreement

We will make one small, coherent upgrade at a time. After each upgrade, the owner reviews the actual result. Work pauses until explicit approval is given for the next change. Each review report must identify changed files, actual test results, known limitations, and the relevant commit.

## Security

- Never commit API keys, OTP credentials, signing keys, database passwords, or private encryption keys.
- Production OTP must use a real configured provider; development test codes are not production authentication.
- Use reviewed cryptographic protocols and maintained libraries. Do not invent cryptography or claim E2EE before it is implemented and verified.
- Keep user media private and access-controlled. Personal Google Drive storage is not the app's shared backend.

## License

All rights reserved unless a license is added by the project owner.
