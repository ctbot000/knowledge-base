---
title: Electron's findInPage findNext option starts a search session, it does not step to the next match
tags: [electron, browser, find-in-page]
added: 2026-09-01
sources:
  - https://www.electronjs.org/docs/latest/api/web-contents#contentsfindinpagetext-options
---

## Fact

In `webContents.findInPage(text, options)` the `findNext` flag names the wrong
thing. It selects whether the request **begins a new find session**, not whether
it advances:

- `findNext: true` — start a new session and highlight the first match.
- `findNext: false` — continue the session already running, which is what moves
  to the next match.
- option omitted entirely — behaves as a new session, *not* as `false`.

So the first request of a search must never pass `findNext: false`. It is
dropped in silence: the call still returns a request id, but no `found-in-page`
event ever arrives and nothing is highlighted.

## Why it matters

The natural reading of the name produces exactly the inverted wiring — `false`
while typing a query, `true` for the next/previous buttons — and the failure is
asymmetric. Stepping still works, because by then a session exists, so the bug
looks like "the match counter is empty until I press the arrow", which points at
the counter's plumbing rather than at the search request.

Passing no options at all works, so a probe written to isolate the problem often
passes while the real call fails, sending the search for the bug into the IPC or
UI layer instead.

## How to apply

- Name the wrapper's parameter for what it does: take `newSession` and pass it
  through as `findNext`, so the call sites read correctly.
- Send a new session when the query text changes, and a continuation for
  next/previous, with `forward` carrying the direction.
- `stopFindInPage()` ends the session, so the first request after closing and
  reopening a find bar must start a new one again.
- When `found-in-page` never fires, check the flag before the wiring: the event
  is the only signal, and the returned request id is not evidence of anything.
