---
title: An HTTP upgrade hands over bytes already read past the handshake
tags: [http, websocket, protocols, networking]
added: 2026-08-27
sources:
  - https://nodejs.org/api/http.html#event-upgrade
---

## Fact

When a connection is upgraded (WebSocket, CONNECT tunnelling, HTTP/2 over h2c),
the HTTP parser has usually read further than the end of the handshake response.
Those extra bytes are the first bytes of the new protocol, and the API hands them
to you separately from the socket:

- Node: `request.on('upgrade', (res, socket, head) => …)` and the server-side
  `server.on('upgrade', (req, socket, head) => …)` — `head` is that buffer.
- Go: `http.Hijacker` returns a `*bufio.ReadWriter` whose reader may already hold
  buffered bytes; reading the raw `net.Conn` skips them.

Attaching a `'data'` listener to the socket and ignoring `head` loses whatever
arrived in the same TCP segment as the handshake.

## Why it matters

The loss is invisible and timing-dependent. A server that sends nothing until the
client speaks first works every time; a server that pushes a greeting frame
immediately — a snapshot, a hello, a session id — loses it only when that frame
lands in the same segment as the response. Fast loopback and small first frames
make it likely, WAN latency makes it rare, so it survives local testing and then
shows up as a client that hangs waiting for a message the server already sent.

## How to apply

- Feed `head` into the same frame parser the socket data goes through, before or
  immediately after signalling "connected", and never treat the socket as the
  only source.
- Emit the connection-open event first, then replay `head`, so listeners
  registered in the open handler still see those frames in arrival order.
- Reproduce it by having the server write its greeting inside the same tick as
  the handshake response over loopback; that reliably coalesces the two.
