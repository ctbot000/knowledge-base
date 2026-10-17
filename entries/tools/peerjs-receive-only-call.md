---
title: A PeerJS call can receive without sending, given an empty MediaStream and offerToReceive constraints
tags: [peerjs, webrtc, media]
added: 2026-10-17
sources:
  - https://github.com/peers/peerjs/blob/master/lib/peer.ts
  - https://github.com/peers/peerjs/blob/master/lib/negotiator.ts
---

## Fact

`peer.call(id, stream)` (PeerJS 1.5) refuses a missing stream, but an empty
`new MediaStream()` is accepted, and the options' `constraints` are passed to
`createOffer`. With `{ constraints: { offerToReceiveAudio: true,
offerToReceiveVideo: true } }` the offer has receive-only audio and video
sections, so the answering side's `call.answer(itsStream)` sends its tracks
and the caller's `stream` event delivers them.

## Why it matters

A viewer of a one-way stream (a broadcast, a camera feed) otherwise needs
`getUserMedia`, with a permission prompt and a camera light, or a fake canvas
and oscillator stream that wastes upload, just to place the call. Without the
constraints the offer has no media sections and the call connects with
nothing on it.

## How to apply

```js
const call = peer.call(stationId, new MediaStream(), {
  constraints: { offerToReceiveAudio: true, offerToReceiveVideo: true },
});
call.on('stream', (s) => { if (video.srcObject !== s) video.srcObject = s; });
```

The station answers each call with the same captured stream
(`video.captureStream()`, a camera, a canvas).
