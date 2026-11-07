---
title: A WebGL game can film its own cutscenes offline in headless Chrome, frames piped to ffmpeg and sound from an OfflineAudioContext
tags: [webgl, ffmpeg, puppeteer, web-audio, video]
added: 2026-11-07
---

## Fact

A browser game's renderer can make real video files of scripted scenes with
no screen recorder: drive a page in headless Chrome, step the scene on a
clock of the film's own (pass each frame's `dt` yourself instead of reading
real time), draw the WebGL canvas into a 2D canvas in the same task as the
render (captions and fades go on there), return `toDataURL('image/jpeg')` from
`page.evaluate`, and write the decoded bytes to ffmpeg's stdin
(`-f image2pipe -c:v mjpeg -framerate 30 -i -`). The soundtrack comes from an
`OfflineAudioContext` in the same page, rendered faster than real time, encoded
as a WAV in the page and muxed in with `-shortest`.

## Why it matters

Real-time capture drops frames and records whatever the machine could manage;
offline stepping is exact and repeatable, and with the GPU (Chrome's
`--use-angle=metal` on macOS) a 1080p-internal frame takes well under 100 ms, so
a minute and a half of film renders in about a minute. The game's own models,
maps and effects are reused, so the film never drifts from the game.

## How to apply

- Read the canvas back right after drawing, in the same task; without
  `preserveDrawingBuffer` it is cleared once the frame is presented.
- Render at 1.5x and let the 2D `drawImage` scale down: cheap anti-aliasing.
- Anything in the scene that reads `performance.now()` or `Math.random()` is
  not under the film's clock: give it time explicitly, or accept the variance.
- Encode H.264 + AAC (`-pix_fmt yuv420p -movflags +faststart`) for playback in
  every browser, `-tune animation` for flat-shaded scenes, and normalise the
  sound (`-af loudnorm=I=-18:TP=-1.5`): synthesised mixes come out quiet.
- On the page that plays it, try `play()` with sound and fall back to muted
  with a tap-for-sound button; a rejected `play()` is the autoplay policy.
