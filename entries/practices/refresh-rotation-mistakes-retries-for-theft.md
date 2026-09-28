---
title: Refresh token rotation reads a lost response or a second tab as token theft
tags: [auth, security, oauth]
added: 2026-09-28
sources:
  - https://www.rfc-editor.org/rfc/rfc9700#section-4.14.2
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API
---

## Fact

With rotating refresh tokens, the server treats a replayed, already-spent
token as proof that two parties hold the session, and it revokes the session.
Two honest clients produce exactly that replay: one that retries after the
refresh response was lost, and two tabs sharing one stored token that refresh
at the same moment.

## Why it matters

Players get signed out at random, and reports about it look like flaky
networking. Where the refresh token is the only credential, as with an
anonymous or guest account, the revocation loses the account for good.

## How to apply

- Server: accept a replay of a token within a short grace period (tens of
  seconds) after it was replaced, and issue a fresh token instead of revoking.
  Count the grace from the first replacement, so retries cannot extend it.
- Server: keep the hash of every replaced token for the session's lifetime,
  so a replay after the grace still revokes the session.
- Browser client: serialize refreshes across tabs with the Web Locks API
  (`navigator.locks.request(name, fn)`). Inside the lock, re-read the stored
  tokens: if another tab already refreshed, use its result instead of
  spending the old token.
- Test it: two clients over one storage refreshing concurrently must make one
  refresh call, and the session must survive.
