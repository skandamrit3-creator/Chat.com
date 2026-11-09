# Chat.com architecture decisions

## Product boundary

Chat.com is a separate product and repository. COSMIC AI may later integrate through a documented, authenticated API; it is not a dependency of the messaging core.

## Service boundaries

- Flutter client: presentation, navigation, local cache, secure device-side key storage.
- FastAPI: identity, profiles, devices, conversations, message APIs and authorization.
- Realtime gateway: authenticated WebSocket sessions and event delivery.
- PostgreSQL: durable application data.
- Redis: ephemeral presence, rate limiting and asynchronous coordination.
- Private object storage: encrypted media blobs with short-lived authorized access.
- Push provider: generic notification payloads that avoid leaking message content.

## Security requirements before public launch

1. OTP verification must have abuse controls, rate limits and provider-side fraud protection.
2. Sessions must be revocable per device; refresh tokens must be rotated and stored securely.
3. Conversation membership and authorization must be checked server-side on every operation.
4. End-to-end encryption must use a reviewed protocol and vetted libraries. Do not invent cryptography.
5. Backups must be separately encrypted with user-controlled recovery material.
6. Media objects must be private by default; never expose permanent public URLs.
7. Logs must exclude OTPs, access tokens, message bodies and encryption secrets.

## Storage note

Google One / personal Google Drive quota is not an application database or a shared backend bucket. Chat.com requires its own backend database and private object storage account. Never connect a user's personal Drive in a way that exposes private files to other app users.

## Milestones

- M0: repository skeleton, health endpoint, starter app, CI.
- M1: phone OTP, user profile, device/session model.
- M2: direct conversations, durable messages, WebSocket delivery and offline sync.
- M3: groups, media upload pipeline and delivery receipts.
- M4: reviewed E2EE and encrypted backup.
- M5: calls, channels, status and communities.
- M6: optional AI features and COSMIC integration.
