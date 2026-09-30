---
title: A string split at an arbitrary index can cut a surrogate pair, and each half is sent as U+FFFD
tags: [unicode, websocket, webrtc, protocols]
added: 2026-09-30
sources:
  - https://websockets.spec.whatwg.org/#dom-websocket-send
  - https://w3c.github.io/webrtc-pc/#dom-rtcdatachannel-send
  - https://webidl.spec.whatwg.org/#idl-USVString
---

## Fact

JavaScript strings are UTF-16, so a character outside the Basic Multilingual
Plane (most emoji, many CJK extension characters) is two code units. Slicing
at a fixed length, as chunking for a size limit does, can end one piece with
the first half and start the next with the second. `WebSocket.send`,
`RTCDataChannel.send` and `TextEncoder` all take a USVString, so each lone half
is replaced with U+FFFD before it is encoded. The reassembled text has two
replacement characters where the emoji was, and nothing throws.

## Why it matters

The corruption is rare and content-dependent: it needs a non-BMP character to
straddle a piece boundary, so it passes every test with ASCII fixtures and
shows up as a mangled name or a JSON parse error only for some users. It looks
like a decoding bug on the receiving side, whose code is in fact correct.

## How to apply

- When cutting at index `end`, step back one if the unit before it is a high
  surrogate:
  ```js
  const c = text.charCodeAt(end - 1);
  if (end < text.length && c >= 0xd800 && c <= 0xdbff) end--;
  ```
- Or encode first and split the bytes, sending binary frames.
- Test chunking with a payload made of emoji and a piece size that is odd.
