---
title: EventSource retries a dropped stream forever but gives up for good on an HTTP error
tags: [browser, server-sent-events, networking]
added: 2026-09-24
sources:
  - https://html.spec.whatwg.org/multipage/server-sent-events.html#fail-the-connection
  - https://developer.mozilla.org/en-US/docs/Web/API/EventSource/error_event
---

## Fact

When a server-sent-events connection drops, the browser reconnects by itself,
waiting the `retry:` interval between attempts. But when an attempt gets a
response that is not `200` with `Content-Type: text/event-stream` (a 401, a
404, a 500), the browser *fails the connection*: `readyState` becomes `CLOSED`
and it never tries again. Both cases fire the same bare `error` event.

## Why it matters

A page whose server restarted with a new token or key in the URL, or whose
route now answers 404, goes silently dead: the `error` event looks exactly like
a network blip, so a "reconnecting…" banner stays up forever. The opposite
mistake, closing the source on every `error`, throws away the free reconnect
after a real blip.

## How to apply

- In `onerror`, read `source.readyState`. `CONNECTING` means the browser is
  retrying; show an offline state and wait. `CLOSED` means it was refused.
- On `CLOSED`, ask why with a plain `fetch` of the same endpoint or a cheap
  probe: 401 or 404 means the session is gone, so tell the user instead of
  spinning; a network error means recreate the `EventSource` after a delay.
- A server that wants clients to stop reconnecting on purpose can answer 204.
