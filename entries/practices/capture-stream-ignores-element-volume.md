---
title: In Chrome, a media element's captureStream() carries its audio whatever the element's muted or volume
tags: [media, webrtc, browser]
added: 2026-10-17
sources:
  - https://w3c.github.io/mediacapture-fromelement/#html-media-element-media-capture-extensions
---

## Fact

`HTMLMediaElement.captureStream()` in Chrome captures the media's audio
before the element's own output stage: setting the element's `muted = true`
or `volume = 0` silences it locally, but the captured audio track stays at
full level. (Verified in Chrome by measuring the received track with an
`AnalyserNode` while toggling both.)

## Why it matters

A page that streams a video it plays (a broadcast station, a screen-share
preview) can play it silently for the operator without silencing every
viewer — or, assuming the opposite, offers a volume control that
looks like it turns everyone down and does nothing for them.

## How to apply

- Start the local player muted; the viewers still hear it.
- Do not present the local volume as a broadcast volume. To change what
  viewers hear, route the audio through Web Audio (`createMediaElementSource`
  → `GainNode` → `createMediaStreamDestination`) and send that track.
- Check other browsers before relying on it: Firefox's `mozCaptureStream()`
  behaves differently.
