---
title: Post-processing render targets made at 1×1 and sized only in resize() stay 1×1 when the chain is rebuilt elsewhere
tags: [threejs, webgl, postprocessing]
added: 2026-11-18
---

## Fact

A common pattern creates the scene's render target and the pass buffers at
1×1 and sizes them in the window's resize handler. If the chain is later torn
down and rebuilt somewhere else — a scene or quality change that switches
passes, shadow bounds or tone mapping — the new targets keep their 1×1 size
until the next resize. The output pass then stretches that single texel over
the screen: every frame is one flat colour that shifts with the camera.

## Why it matters

It happens only at the qualities that use post-processing, and only after the
rebuild, so it looks like a shader or lighting bug in the new scene. Hiding the
new content changes nothing, which sends the search the wrong way.

## How to apply

- Follow every rebuild of the chain with the same sizing call the resize
  handler makes, or create the targets at the drawing buffer's size.
- To diagnose a flat-coloured frame, read the scene target's `width` and
  `height` before suspecting materials.
