---
title: Framing a box in a perspective camera is a per-corner solve, not a bounding sphere
tags: [3d, camera, layout]
added: 2026-09-08
---

## Fact

The usual fit, `distance = radius / sin(fov / 2)` around a bounding sphere, is
orientation-blind. For anything that is not roughly cubic it backs the camera off
much further than needed, and the subject sits small in the middle of an empty
frame — most visibly in a portrait window, where the horizontal field is the
tight one and the sphere ignores which way the long axis points.

The exact answer is cheap. With the camera at distance `d` from the look-at
point along `away`, a corner `p` measured from that point has depth
`p·forward + d`, so it is inside the frustum when

```
d >= |p·right| / tanH - p·forward        (and the same with up / tanV)
```

Take the maximum over the eight corners. Recompute when the angle or the aspect
changes; it is a few dozen operations.

## Why it matters

Projecting the box's extents onto the camera axes — the obvious improvement over
a sphere — is an orthographic approximation, and it clips: in perspective the
near corners splay outward, so the corner closest to the camera leaves the frame
while the arithmetic says it fits. The per-corner form has the depth term that
accounts for exactly this.

## How to apply

- Fit the box you actually want on screen, not the outermost trim. On a diagonal
  view only the corners reach the frame edge, so fitting a decorative border
  shrinks the subject for the sake of geometry nobody looks at.
- Pick the viewing angle from the aspect ratio: point a long subject away from
  the camera in a portrait frame and across it in a landscape one.
- Multiply by a small margin (a few percent) rather than a large one; the solve
  is exact, so the margin is only for what sticks out of the box.
