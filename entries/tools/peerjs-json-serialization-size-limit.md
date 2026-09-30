---
title: PeerJS's JSON serialization refuses any message of 16,300 bytes or more
tags: [peerjs, webrtc, serialization]
added: 2026-09-30
sources:
  - https://github.com/peers/peerjs/blob/master/lib/dataconnection/BufferedConnection/Json.ts
  - https://github.com/peers/peerjs/blob/master/lib/util.ts
---

## Fact

A `DataConnection` opened with `serialization: 'json'` (PeerJS 1.5) encodes each
message and, if the UTF-8 result is 16,300 bytes or more (`util.chunkedMTU`),
drops it and emits an `error` of type `message-too-big` on the sender's
connection. `send()` itself returns normally. Only `binary` serialization
chunks large messages; `raw` sends them as they are.

## Why it matters

Chat lines, pings and small updates all fit, so a protocol works in testing
until the first large message: typically the full-state snapshot a newcomer
or a reconnecting player needs. The receiver simply never hears it and waits
for ever, which reads as a stuck handshake or a signaling problem, while the
evidence sits in an `error` handler on the other machine that nobody logs.

## How to apply

- For JSON payloads that can grow, open the connection with
  `serialization: 'raw'`, `JSON.stringify` yourself, and split long strings
  into pieces well under 16 KB with an id, index and count to reassemble them.
  Keep pieces under 16 KB anyway: larger ones are cut when Firefox sends to Chrome.
- Split strings where they cannot tear a surrogate pair: see
  [[split-string-cuts-surrogate-pairs]].
- Log `conn.on('error')` on both ends, and test with a state the size of the
  biggest real one, not the empty initial state.
