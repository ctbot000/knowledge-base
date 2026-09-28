---
title: PeerServer reports a connect to an absent peer once per undeliverable message, five seconds late
tags: [peerjs, webrtc, retries]
added: 2026-09-28
sources:
  - https://github.com/peers/peerjs-server/blob/master/src/messageHandler/handlers/transmission/index.ts
  - https://github.com/peers/peerjs-server/blob/master/src/services/messagesExpire/index.ts
---

## Fact

PeerServer does not reject a message for an id that is not registered. It
queues it, delivers it if that id registers within `expire_timeout` (5 s by
default), and otherwise answers EXPIRE. Each queued message expires on its
own: the offer and every trickled ICE candidate. One failed `peer.connect()`
or `peer.call()` therefore raises `peer-unavailable` several times, spread over
the seconds after the first.

## Why it matters

A retry loop that reacts to every `peer-unavailable` dials several times per
failure, and the late echoes of one attempt tear down the next attempt as it
starts. It reads as flapping connectivity. The delay also means that learning
"that peer is offline" takes at least five seconds.

## How to apply

- Act on the first `peer-unavailable` of an attempt. Ignore it while a retry
  is already scheduled, and for the first few seconds of a new attempt: the
  server holds messages for 5 s, so anything sooner is an echo.
- Retry on a timer of a few seconds. An offer sent just before the other side
  registers is still delivered from the queue.
- Keep an overall connect timeout as well; not every failure is reported.
