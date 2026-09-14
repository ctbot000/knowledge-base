---
title: In a 3D scene, assert that every interactive cell round-trips from its own pixel back to itself
tags: [3d, testing, game-design, input]
added: 2026-09-14
---

## Fact

The contract of a 3D board is that the thing under the cursor is the thing the
program acts on. In 2D that is arithmetic and holds by construction; in 3D it
runs through a projection, its inverse, a ray and a plane intersection, and any
of those can be subtly wrong in a way that still looks plausible on screen.

It is cheap to assert exactly, and the assertion is the contract itself:

```
for each cell:
  pixel = project(centre of cell)
  if pixel is off screen: skip
  assert pickCell(rayThroughPixel(pixel)) == cell
```

Run it at several camera orientations — the identity view hides sign errors
that only appear once the camera is yawed past 90°.

## Why it matters

The obvious alternative, clicking and looking, passes on a near-top-down view
where projection error is under a cell's width, and then fails after the
player orbits — the one state that is tedious to reproduce by hand. An
off-by-one in the inverse projection also tends to be small near the screen
centre and large at the edges, so a handful of spot checks confirm it.

Surfaces at different heights are the other half. Where a scene has raised
tiles and sunken paths, a picker resolving everything against one plane is
skewed by the height difference, which shows only near grazing angles.

## How to apply

- Make the maths a pure module — projection, ray construction, cell
  resolution — separate from the GPU, so the whole round-trip runs headlessly
  in CI rather than needing a browser.
- Sweep yaw across all four quadrants, plus a shallow and a steep pitch, and
  a zoom either side of the default.
- Assert a floor on how many cells were actually on screen, or a projection
  that puts everything behind the camera passes by testing nothing.
- Project each cell at the height its own surface sits at, so the test covers
  the multi-level case rather than assuming one ground plane.

Related: [[element-click-does-not-hit-test]], [[perspective-aim-needs-a-cone]].
