---
title: PeerJS fires a call's stream event once per remote track, and setting srcObject again aborts the play() in flight
tags: [peerjs, webrtc, media]
added: 2026-10-17
sources:
  - https://github.com/peers/peerjs/blob/master/lib/negotiator.ts
  - https://developer.chrome.com/blog/play-request-was-interrupted
---

## Fact

A PeerJS 1.5 `MediaConnection` emits `stream` from the peer connection's
`ontrack`, so a call carrying audio and video emits it twice, with the same
`MediaStream` both times. Assigning that stream to a media element's
`srcObject` again starts a new load, which rejects the `play()` promise from
the first assignment with `AbortError: The play() request was interrupted by
a new load request`.

## Why it matters

The common pattern catches a rejected `play()` as an autoplay refusal and
falls back to muted playback with a "tap for sound" prompt. With two tracks
that fallback fires every time, although the browser would have allowed
sound: the video plays silently and the user is asked for a tap that was
never needed.

## How to apply

- In the `stream` handler, return early when `video.srcObject === stream`.
- Treat `AbortError` from `play()` as "superseded", not as "autoplay
  blocked"; only `NotAllowedError` means the browser refused sound.
