---
title: A ws server connection without an 'error' listener lets one bad client frame end the process
tags: [node, websocket, ws, error-handling]
added: 2026-10-05
sources:
  - https://github.com/websockets/ws/blob/master/doc/ws.md#event-error-1
---

## Fact

When a client sends a frame the `ws` library refuses (unmasked, over
`maxPayload`, invalid UTF-8 in a text frame), the server-side `WebSocket`
closes the connection with the matching code (1002, 1009, 1007) and also emits
`'error'`. A connection with no `'error'` listener turns that into an uncaught
exception, so the whole server process exits.

## Why it matters

Handlers are usually written for `'message'` and `'close'` only, and normal
clients never send bad frames, so nothing shows up in development. Any client
can then crash the server with a single frame header claiming a payload over
the limit, which disconnects every other user too.

## How to apply

- Attach a listener to every accepted connection, even an empty one: the close
  has already been handled.

  ```js
  wss.on('connection', (ws) => {
    ws.on('error', () => {}); // ws closes the connection itself
  });
  ```

- Test it with a raw socket: after the handshake, send only a frame header
  declaring more than `maxPayload` bytes, and assert a close frame with 1009
  and a server that still answers.
