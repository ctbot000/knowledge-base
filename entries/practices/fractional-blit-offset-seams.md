---
title: Nearest-neighbour blitting at a fractional offset seams every tile edge
tags: [canvas, graphics, frontend]
added: 2026-09-07
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/imageSmoothingEnabled
---

## Fact

`imageSmoothingEnabled = false` does not make `drawImage` exact; it makes it
nearest-neighbour. At a non-integer destination coordinate the destination grid
sits at a fraction of a source pixel, so the sampler drops or doubles a row and
a column at the edges of whatever it draws.

Blitting a tile grid as `ox + x * TILE` therefore puts every tile on the same
wrong phase when `ox` is fractional, and the result is a regular pattern of
one-pixel seams across the whole surface.

It only appears while the offset is fractional — a camera panning at a speed
that is not a whole number of pixels per frame, an interpolated screen
transition, a sub-pixel entity position — so it exists during motion and is gone
the moment anything stops. Device pixel ratio moves the threshold rather than
removing it: at DPR 2 a `.5` offset lands on a whole device pixel and looks
clean, which is why it can be invisible on the machine it was written on.

## Why it matters

The artifact reads as a texture problem, not a positioning one. The usual
response is to go and pad or extrude the sprite atlas against bleed, which is a
real technique for a different bug and does nothing for this one, while the
actual fix is one line in the draw call. And because it vanishes whenever the
scene stops, it survives most screenshots taken to investigate it.

## How to apply

- Round the offset once, where the blit loop starts — not per tile, which makes
  tiles jitter against each other:
  `const ox = Math.round(offsetX);`
- Keep the fractional value in the camera or entity for the simulation. Round
  only at the point of drawing, so movement stays smooth.
- If genuine sub-pixel motion is wanted, render the scene to one buffer and
  offset that buffer, so there is exactly one resample instead of one per tile.
