# Chat.com — UI Guidelines

## Visual direction

Build a modern, premium, calm messaging interface. The interface should feel polished and recognizable without copying another messaging app's exact layout or branding.

- Use Material 3 foundations with a custom Chat.com color system.
- Use generous but efficient spacing; prioritize readability over decoration.
- Use rounded surfaces consistently, restrained elevation, and clear visual hierarchy.
- Use a light theme first with a carefully tuned dark theme as a later visual pass.
- Use one coherent icon family and consistent stroke/filled states.
- Avoid excessive gradients, glass effects, decorative animations, and crowded dashboards.

## Main screens

### Chats
- App identity and profile access in the top bar.
- Search entry point.
- Conversation rows with avatar, name, latest message, time, and unread count.
- Clear empty state with a direct start-chat action.
- Pull-to-refresh only when backed by actual refresh behavior.

### Conversation
- Clear contact identity and connection/call actions.
- Distinct incoming and outgoing message bubbles.
- Readable timestamps and delivery state.
- Composer pinned above the keyboard and safe area.
- Attachment and voice-note actions must not be decorative dead buttons.
- Support long messages, links, and accessibility text scaling.

### Contacts
- Permission request only when needed and with an explanation.
- Manual username/phone discovery fallback.
- Do not upload address books without clear consent.

### Settings
- Profile, privacy, notifications, appearance, linked devices, storage, help, and account actions.
- Destructive actions require confirmation.

## Interaction standards

- Every visible control must work or be clearly disabled with an explanation.
- Show loading, empty, success, offline, and error states.
- Preserve draft text when navigating away or losing connectivity.
- Never use fake unread counts, fake presence, or fake delivery receipts in connected mode.
- Respect Android system back, keyboard, and edge-to-edge insets.
- Animations should be short, purposeful, and avoid blocking input.

## Review criteria

A screen is ready for user review when its layout is coherent, all visible controls have defined behavior, text does not overflow on a narrow phone, and loading/empty/error states are considered.
