---
title: PeerServer takes a reconnect under a still-registered id without sending OPEN, so PeerJS never fires `open`
tags: [peerjs, webrtc, signaling]
added: 2026-09-28
sources:
  - https://github.com/peers/peerjs-server/blob/master/src/services/webSocketServer/index.ts
---

## Fact

When a socket arrives for an id that PeerServer still has registered, and its
token matches, the server moves the session to the new socket and sends
nothing. OPEN goes out only when a client is registered from scratch. The
PeerJS client waits for OPEN, so `peer.open` stays `false` and `open` never
fires, although messages already route to the new socket.

## Why it matters

Two ordinary paths hit it. `peer.reconnect()` after a network drop reuses the
token while the server still holds the dead socket (until its heartbeat
timeout, 90 s by default). Persisting the token to reclaim a fixed id after a
page reload does the same whenever the old socket has not closed yet. Code
that waits for `open`, to show "live" or before dialing, then waits forever,
where a different token would have failed loudly with `unavailable-id`.

## How to apply

- Do not reuse tokens across page loads. Let a fresh token hit
  `unavailable-id` and retry with backoff until the old session expires.
- After `reconnect()`, give `open` a few seconds. If it has not come but the
  socket is open (`peer.socket._wsOpen()` in PeerJS 1.5, an internal), treat
  the peer as connected; otherwise destroy it and create a new one.
- Replace, rather than reconnect, peers whose id is disposable (viewers,
  callers): a new random id cannot collide.
- On shutdown, `peer.disconnect()` first so the server frees a fixed id at
  once, then close the peer connections; a quick restart then does not collide.
