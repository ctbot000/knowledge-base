---
title: Chrome runs a page's getUserMedia requests one at a time, so one that never settles blocks every later request
tags: [webrtc, getusermedia, browser, debugging]
added: 2026-09-28
sources:
  - https://github.com/chromium/chromium/blob/main/third_party/blink/renderer/modules/mediastream/user_media_client.cc
---

## Fact

Chrome puts a frame's `getUserMedia` calls on one queue and processes them
sequentially (`getDisplayMedia` has a separate queue). A request that never
settles, because a prompt is never answered or a device never opens, leaves
every later camera and microphone request in that frame pending as well. No
error is raised anywhere.

## Why it matters

The symptom points at the wrong call: a camera that "will not start" is
waiting behind an earlier microphone request. One way to get there: on macOS,
Chrome's fake audio device (`--use-fake-device-for-media-stream`) has been
seen to leave `getUserMedia({ audio })` pending indefinitely under automation,
headless and headful alike, after which even a `{ video }` request that works
on its own hangs.

## How to apply

- When a `getUserMedia` call hangs, look for an earlier call in the same frame
  that never settled; a reload is the only reset.
- In diagnostics, race each call against a timer and log which one is stuck.
  A pending request cannot be cancelled, only identified.
- In automation, fake the devices inside the page instead of relying on the
  browser's fake audio device: [[fake-camera-via-canvas-capturestream]].
