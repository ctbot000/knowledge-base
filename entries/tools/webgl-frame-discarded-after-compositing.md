---
title: A WebGL canvas discards its frame after compositing, so a later read comes back blank
tags: [webgl, testing, browser]
added: 2026-09-08
sources:
  - https://registry.khronos.org/webgl/specs/latest/1.0/#2.2
---

## Fact

The WebGL drawing buffer is presented and then cleared. With the default
`preserveDrawingBuffer: false`, its contents are undefined once the compositor
has taken them, so `readPixels`, `toDataURL` and `drawImage(canvas, …)` return
the frame only while still inside the task that drew it. Afterwards they come
back blank even though the render was perfect.

This collides with the two usual ways of checking a canvas, and both fail the
same way. A screenshot goes through the compositor, which a hidden or occluded
surface may never run, so the image is empty. A deferred read of the buffer is
empty for the unrelated reason above. Either way the evidence says "nothing was
rendered".

The probe that separates them is `readPixels` issued in the same task as the
draw. It reads the buffer before presentation, and so answers *did the GPU
produce this frame* independently of *did the frame reach the screen*.

## Why it matters

For the DOM or a 2D canvas there is committed state to fall back on —
`getComputedStyle`, `textContent`. A WebGL canvas has none: the pixels are the
only evidence it offers, and the default configuration destroys them.

So a blank capture sends you into the matrices, the winding order, the culling
mode and the shaders, none of which is wrong, and every subsequent "fix" is
validated against another blank capture.

## How to apply

- Sample a handful of points with `readPixels` in the same task as the draw.
  Anything other than the clear colour means the renderer works and the problem
  is presentation, not rendering.
- Set `preserveDrawingBuffer: true` on any canvas that has to be captured;
  without it `toDataURL` and `drawImage` from it are blank. It costs one buffer
  copy per frame, which is nothing at modest resolutions.
- To capture what a viewer would see from layered canvases, composite them into
  an offscreen 2D canvas yourself instead of screenshotting the page.
- The presentation half of this is [[hidden-surface-delivers-no-frames]] and
  [[screenshot-lags-committed-dom-state]].
