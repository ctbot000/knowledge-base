---
title: Drawing many frames in one synchronous call leaves a software GPU seconds behind, and no new frame shows until it catches up
tags: [testing, automation, webgl, browser, ci]
added: 2026-10-02
---

## Fact

WebGL calls only queue commands for the GPU process, so a test hook that steps
an app N times in one call and draws every step returns almost at once. With a
real GPU the queue drains as fast as it fills. With software rendering
(SwiftShader, which headless Chrome uses on a runner with no GPU) each queued
frame costs tens to hundreds of milliseconds of CPU, so the call leaves seconds
of work behind it, and the page presents no new frame, and runs no
`requestAnimationFrame` callback, until all of it is done.

## Why it matters

The test carries on while the page is frozen. A wait polled on animation frames
takes the whole backlog, and anything timed on the wall clock that only a frame
would draw can run out unseen: a 4.5 s speech bubble said right after a 40-step
camera move was never drawn, because the next frame came 4.6 s later. It fails
as a polling timeout on the slow runner only, far from the stepping that caused
it, and in a trace the page's own main thread looks idle.

## How to apply

- Draw only the last of the steps. Run everything else every step, and do what
  `render()` does besides the picture (three.js: update the scene's and the
  camera's world matrices). What must still run per step:
  [[driven-harness-must-drive-the-frame]].
- If a batch has to draw, wait two animation frames before anything timed; how
  long that takes is the size of the backlog.
- In a Chrome trace the backlog is long `CommandBuffer::Flush` slices on the GPU
  process's main thread. On macOS every SwiftShader frame shows as a
  `readPixels` and `finishImpl` pair, normally tens of milliseconds long.
- To reproduce it on a fast machine: [[taskpolicy-slows-a-browser-to-ci-speed]].
