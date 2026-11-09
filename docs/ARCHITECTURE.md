# Chat.com architecture decisions

## Product boundary

Chat.com is an independent messaging product. COSMIC AI may later integrate through a documented, authenticated, user-authorized API; the messaging core must not depend on COSMIC.

## Service boundaries

- Flutter client: presentation, navigation, local cache, secure device-side storage.
- FastAPI: identity, profiles, devices, conversations, message APIs, and authorization.
- Realtime gateway: authenticated WebSocket sessions and event delivery.
- PostgreSQL: durable application data.
- Redis: ephemeral presence, rate limiting, and asynchronous coordination.
- Private object storage: encrypted media blobs with short-lived authorized access.
- Push provider: generic notification payloads that avoid leaking message content.

## Security requirements

1. OTP verification needs abuse controls, rate limits, and provider-side fraud protection.
2. Sessions must be revocable per device; refresh tokens must be rotated and stored securely.
3. Conversation membership and authorization must be checked server-side on every operation.
4. End-to-end encryption must use a reviewed protocol and vetted libraries. Do not invent cryptography.
5. Backups must be separately encrypted with user-controlled recovery material.
6. Media objects must be private by default; never expose permanent public URLs.
7. Logs must exclude OTPs, access tokens, message bodies, and encryption secrets.

## Storage note

Google One / personal Google Drive quota is not an application database or shared backend bucket. Chat.com requires its own backend database and private object storage account. Never connect a personal Drive in a way that exposes private files to app users.

## Product map and structure

See [MIND_MAP.md](MIND_MAP.md), [PRODUCT_SPEC.md](PRODUCT_SPEC.md), [FILE_STRUCTURE.md](FILE_STRUCTURE.md), [UI_GUIDELINES.md](UI_GUIDELINES.md), and [SECURITY_BASELINE.md](SECURITY_BASELINE.md).

## Implementation discipline

Development is intentionally incremental and owner-reviewed. Implement one small, testable improvement, report the exact changes and verified checks, then pause for approval. The detailed agreement is in [REVIEW_PROCESS.md](REVIEW_PROCESS.md).
