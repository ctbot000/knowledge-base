---
title: A camera solved to fill the frame converges on a face-on view and throws the perspective away
tags: [3d, camera, game-design]
added: 2026-09-10
---

## Fact

Auto-framing is usually written as an optimisation: search the camera's angle
and distance, keep whatever puts the most of the subject on screen. For a
subject that is broadly planar — a board, a playfield, a floor plan, a page —
that objective has one maximum, and it is looking straight down the plane's
normal. Projected area is largest face-on, and every degree of obliqueness
costs it.

So the solver reliably returns the most orthographic view available to it. The
framing is optimal and the picture is flat: the depth cues the 3D view existed
to provide are exactly what the objective was discarding.

## Why it matters

Both halves look correct in isolation. The fill number really is higher, and
nothing is wrong with the projection, so the result reads as "the perspective
is too weak" and gets chased in field of view or in lighting, which cannot fix
it — the angle is the variable, and it was chosen deliberately.

It bites hardest on a portrait viewport, where the shortfall from an oblique
angle is largest, so the flattening appears on phones and in narrow panes and
not on the developer's wide window.

## How to apply

- Constrain the search to the range of angles that still read as the view you
  want, and optimise fill only inside it. A clamp is the fix, not a workaround:
  the objective is genuinely incomplete.
- Prefer solving distance and lens shift, which do not change the read, over
  solving orientation, which does.
- Recentre by shifting the frustum (`m[8]`, `m[9]` in a column-major projection)
  rather than moving the camera; it slides the image without touching the
  perspective, and shifts NDC by exactly the amount set.
- Fit against every corner of the subject's box, not a bounding sphere, which
  is orientation-blind — see [[framing-a-box-is-a-per-corner-solve]].
