---
title: A swallowed storage write needs an in-memory copy, or the next read contradicts it
tags: [storage, caching, error-handling, frontend]
added: 2026-08-29
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
---

## Fact

Wrapping a storage call in `try/catch` stops it from throwing; it does not make
the write happen. `localStorage` throws on every access in private-browsing
modes, under blocked-cookie settings, and from opaque origins such as `data:`
and sandboxed frames — so a helper that catches and returns turns a failed write
into a silent one.

The bug appears at the next read. Code that treats the store as its source of
truth re-reads the key, gets the pre-write value, and contradicts the write it
just reported as successful — inside a single session, with no error anywhere.

## Why it matters

The failure lands on whatever the value gates, so it presents as broken logic
rather than broken persistence: a flag that will not set, a step that reopens
after being completed, a preference that reverts the moment it is read back.

It also survives testing, because development happens in an ordinary window
where the writes succeed. Only the users whose storage is unavailable see it,
and for them the feature is not degraded but wrong.

## How to apply

- Keep the value in memory and treat storage as write-through: read it once to
  seed, serve every subsequent read from the field, and persist on change.
- Then a storage failure costs only persistence across reloads, which is the
  honest consequence, instead of corrupting the running session.
- Distinguish "absent" from "zero" when seeding. `JSON.parse(null)` is `null` and
  a stored `0` is falsy, so `stored || DEFAULT` silently resets a legitimate zero;
  test the type or compare against `null` explicitly.
- Probe once at startup if the UI should say so, rather than at each call site.
