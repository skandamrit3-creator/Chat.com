# Chat.com — User Review Process

## Working agreement

Development proceeds in small visible upgrades. The project owner reviews each result before the next upgrade begins.

1. Select one small, coherent improvement.
2. Inspect related files and existing behavior before editing.
3. Implement the improvement without silently expanding scope.
4. Run the relevant checks where execution is available.
5. Commit the changes with a clear message.
6. Report exactly what changed, what was tested, and what remains incomplete.
7. Stop and wait for the project owner's explicit approval before starting another upgrade.

## Review gates

- A request to review, inspect, or explain does not authorize the next implementation change.
- “Yes”, “approved”, or a clear equivalent authorizes the next specifically described upgrade.
- If feedback requests changes, fix only the requested issues and return for review.
- Never claim a build, test, deployment, OTP delivery, encryption, or live message flow succeeded unless it was actually executed and verified.
- Keep the default branch stable. Use a review branch for changes that could disrupt an accepted version.

## Definition of done for a review

Each review report states:
- Files added, changed, or removed.
- User-visible behavior.
- Checks actually run and their results.
- Known limitations and required external setup.
- Exact GitHub commit or file links.

## Scope discipline

Do not add large future features merely because they appear in the mind map. Keep the current review small enough to inspect on a phone. Preserve accepted behavior unless the owner explicitly approves a redesign.
