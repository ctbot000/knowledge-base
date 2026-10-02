---
title: A fixed peer id on a public PeerServer belongs to whoever registers it first, so clients must authenticate the peer before sending
tags: [peerjs, webrtc, signaling, security]
added: 2026-10-03
sources:
  - https://github.com/peers/peerjs-server/blob/master/src/services/webSocketServer/index.ts
---

## Fact

PeerServer checks only the API key, which every client of a public server
shares, and that the id is free and well formed. While the service
that normally holds a well-known id is offline, anyone can register that id,
and every client that dials it reaches them instead. The encrypted data
channel does not help: it is encrypted to whoever answered.

## Why it matters

A client that dials a fixed id to upload data (a backup server, a bot, a
relay) hands that data to a squatter the moment the real peer goes offline,
and nothing on the client side looks wrong.

## How to apply

- Pin the peer's public key in the client (shipped with the app, not taken
  from the URL or from the peer).
- On every connection, send a fresh random nonce first and send nothing else
  until the peer returns a signature over the nonce and its own id; close
  otherwise. Signing the id as well keeps a key shared by several services
  from vouching for one under another's id.
- WebCrypto ECDSA P-256 works for this in browsers and in Node
  (`crypto.subtle` in both): `sign` and `verify` with SHA-256 use the same raw
  64-byte signature on both sides, so no DER conversion is needed.
- Back off for a long time after a failed check; the real peer cannot come
  online under that id until the squatter leaves.
