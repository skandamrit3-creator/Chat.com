# Chat.com — Complete Product Mind Map

Chat.com is an Android-first, privacy-focused communication app. The product is independent from COSMIC AI; optional integration may be added later through a secure, user-authorized API.

```mermaid
mindmap
  root((Chat.com))
    Identity and accounts
      Phone number registration
      OTP verification
      Profile and username
      Contacts and discovery
      Device sessions
      Account recovery
    Conversations
      One-to-one chats
      Group chats
      Communities
      Channels
      Pinned and archived chats
      Search
    Messaging
      Text and emoji
      Replies and threads
      Reactions
      Edit and delete
      Forward
      Scheduled messages
      Delivery and read receipts
      Offline queue and sync
    Media and files
      Camera and gallery
      Photos and video
      Documents
      Voice notes
      Audio playback
      Private object storage
      Upload and download controls
    Calls
      Voice calls
      Video calls
      Group calls
      Screen sharing
      Call history
    Privacy and security
      End-to-end encryption
      Device key management
      Secure local storage
      App lock
      Disappearing messages
      Block and report
      Privacy controls
      Encrypted backup and restore
    Social features
      Status and stories
      Polls
      Communities
      Channel subscriptions
    Productivity
      Reminders
      Message search
      Pinned messages
      Saved messages
      Translation
    Intelligence
      Optional AI assistant
      Conversation summaries
      Smart search
      Spam and abuse detection
      COSMIC AI integration
    App experience
      Android-first Flutter UI
      Themes and wallpapers
      Notifications
      Accessibility
      Localization
      Multi-device experience
    Platform and operations
      FastAPI backend
      PostgreSQL
      WebSocket gateway
      Redis and background jobs
      Push notifications
      Private media storage
      Monitoring and audit logs
      CI and automated tests
      Signed Android releases
      Safe app updates
```

## Product rules

- Phone number plus OTP is the intended sign-in experience. Real SMS verification must use a configured provider; development test codes must never be presented as production verification.
- A message is not considered delivered merely because the sender tapped Send. Delivery states must reflect server/device acknowledgements.
- Private conversations and media must be protected by authorization checks. Public media URLs are not acceptable.
- End-to-end encryption must use a reviewed protocol and maintained implementation. No custom cryptography.
- AI and COSMIC integration are optional and must not weaken the messaging privacy boundary.
- The app must remain useful and responsive on Android phones, including smaller screens.
- Features must be visibly labeled as unavailable until they genuinely work.
