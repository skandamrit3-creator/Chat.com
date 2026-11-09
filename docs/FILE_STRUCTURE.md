# Chat.com — Repository File Plan

This is the target structure. Files are introduced when their implementation is ready; folders and placeholder source files must not pretend to contain working features.

```text
Chat.com/
├── README.md
├── .gitignore
├── .env.example
├── app/                              # Flutter Android client
│   ├── pubspec.yaml
│   ├── analysis_options.yaml
│   ├── android/
│   │   ├── app/
│   │   │   ├── build.gradle
│   │   │   └── src/main/AndroidManifest.xml
│   │   └── settings.gradle
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── app.dart
│   │   ├── core/
│   │   │   ├── config/
│   │   │   ├── theme/
│   │   │   ├── routing/
│   │   │   ├── networking/
│   │   │   ├── storage/
│   │   │   └── widgets/
│   │   ├── features/
│   │   │   ├── onboarding/
│   │   │   ├── authentication/
│   │   │   ├── home/
│   │   │   ├── conversations/
│   │   │   ├── chat/
│   │   │   ├── contacts/
│   │   │   ├── media/
│   │   │   ├── calls/
│   │   │   ├── status/
│   │   │   ├── channels/
│   │   │   ├── settings/
│   │   │   └── privacy/
│   │   └── shared/
│   └── test/
├── backend/                          # FastAPI service
│   ├── requirements.txt
│   ├── .env.example
│   ├── alembic.ini
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   ├── app/
│   │   ├── main.py
│   │   ├── settings.py
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── realtime/
│   │   ├── security/
│   │   └── workers/
│   └── tests/
│       ├── unit/
│       └── integration/
├── docs/
│   ├── MIND_MAP.md
│   ├── FILE_STRUCTURE.md
│   ├── PRODUCT_SPEC.md
│   ├── UI_GUIDELINES.md
│   ├── SECURITY_BASELINE.md
│   ├── ARCHITECTURE.md
│   └── REVIEW_PROCESS.md
├── infra/
│   ├── docker/
│   └── deployment/
└── .github/
    └── workflows/
        ├── backend-ci.yml
        └── app-checks.yml
```

## File responsibilities

### Flutter app
- `main.dart` starts the application; `app.dart` configures the root widget.
- `core/config` owns environment-aware configuration; no secrets are committed.
- `core/theme` owns design tokens, typography, colors, and theme variants.
- `core/routing` owns navigation and route guards.
- `core/networking` owns typed API and WebSocket clients.
- `core/storage` owns local persistence and secure token/key storage.
- Each `features/<name>` folder owns that feature's screens, state, models, and widgets.

### Backend
- `api/v1` contains versioned HTTP routes.
- `database` contains database connection and session management.
- `models` contains persistence models; `schemas` contains validated API contracts.
- `services` contains business rules; `repositories` contains data access.
- `realtime` handles authenticated WebSocket connections and events.
- `security` handles authentication, authorization, rate limits, and key-related interfaces.
- `migrations` contains versioned schema changes. Never rely on production auto-create tables.

### Operations
- `.github/workflows` runs repeatable checks.
- `infra` contains deployment definitions, not secrets.
- `docs` records product behavior, architecture, security decisions, and review checkpoints.

## Rules for adding files

1. Add a file only when it has a defined responsibility and real implementation or useful documentation.
2. Keep feature code modular; avoid a single giant Dart or Python file.
3. Add tests beside the behavior they verify.
4. Keep credentials, signing keys, OTP secrets, private keys, and production URLs out of Git.
5. Update this document when the structure changes.
