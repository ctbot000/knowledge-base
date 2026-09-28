---
title: A camera web app can be driven in automation by returning a canvas stream from getUserMedia
tags: [testing, automation, browser, webrtc]
added: 2026-09-28
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/captureStream
  - https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
---

## Fact

Replacing `navigator.mediaDevices.getUserMedia` in the page with a function
that resolves to `canvas.captureStream(fps)` gives the app a live video track
it cannot tell apart from a camera. Whatever the test draws on that canvas
(a code, a document, a moving scene) arrives through the app's real
`<video>`, frame grabbing and processing path. No browser flags, device, or
permission prompt are involved.

## Why it matters

Automation browsers, embedded panes and CI machines usually have no camera,
and flags like Chrome's `--use-fake-device-for-media-stream` cannot be passed to
a browser the test does not launch. The camera path then goes untested, and it
is where the lifecycle bugs live: stale paused frames, overlays mapped through
`object-fit: cover`, restarts after the tab is hidden.

## How to apply

- Install the override before the app calls `getUserMedia`, and keep redrawing
  the canvas (a timer, not `requestAnimationFrame`, so a hidden surface still
  produces frames). A canvas that stops changing stops producing new frames.
- Change the drawing mid-test to exercise "scan again" and repeated-result
  logic.
- The fake track has no `facingMode`, and `getCapabilities()` reports no torch
  or zoom. Test those branches separately.
