# Chat.com — Security Baseline

## Identity
- OTP delivery and verification must be performed by a real configured identity provider in production.
- Apply per-number, per-IP, and device-aware rate limits.
- Never log or store plaintext OTP values.
- Use short-lived access tokens and rotating, revocable refresh sessions.
- Allow users to view and revoke active devices.

## Authorization and data
- Enforce conversation membership on every read, write, attachment, and realtime subscription.
- Use parameterized database access and strict request validation.
- Keep private media buckets private; issue short-lived authorized access.
- Avoid exposing whether a phone number is registered where that enables account enumeration.

## Encryption
- Use TLS for all network traffic.
- Use platform secure storage for device credentials and key material.
- End-to-end encryption must be implemented with a reviewed protocol and maintained library.
- Do not invent a cryptographic protocol or claim E2EE before implementation and testing.
- Design encrypted backup separately from ordinary server-side database backup.

## Operational safety
- Never commit .env files, tokens, provider credentials, signing keys, or private keys.
- Redact authorization headers, OTPs, message bodies, and secrets from logs.
- Keep audit events for sensitive account and device actions without recording message content.
- Use dependency updates, automated tests, backups, and incident procedures before public launch.

## Privacy defaults
- Collect only data required for the feature.
- Ask before accessing contacts, camera, microphone, photos, and notifications.
- Explain permission purpose at the point of use.
- Do not use a personal Google Drive account as shared application storage.
