---
title: A 3D detail placed at a 2D-looking offset ends up inside the mesh and vanishes silently
tags: [3d, graphics, webgl, frontend]
added: 2026-09-08
---

## Fact

In 2D, draw order decides what is on top, so a face can be painted at any offset
over a body and it will be visible. In 3D there is no draw order to lean on —
position alone decides — and the offsets that look right in a flat sketch land
*inside* the solid.

The gap is bigger than it feels. On an ellipsoid with semi-axes `(a, b, c)`, the
surface at a point that is 34% of the way across and 16% of the way up is still
at `z = c·√(1 − 0.34² − 0.17²) ≈ 0.87c`. An eye placed at `0.62c` — a perfectly
reasonable-looking "on the front of the head" — is entirely swallowed, and so is
anything smaller than the 0.25c it is short by.

## Why it matters

Nothing reports it. The mesh exists, is added to the scene, is lit and is drawn;
it is simply behind an opaque surface. So the symptom is a missing feature with
a healthy scene graph, which reads as "the mesh never got added", "the material
is broken" or "the parent transform is wrong" — three wrong places to look.

It bites hardest when porting layered 2D art, because every offset in the old
code is a plausible-looking constant that now means something different, and the
whole face disappears at once rather than one part at a time.

## How to apply

- Project onto the surface instead of guessing: normalise a direction, scale it
  by the semi-axes, and orient the part outwards (`lookAt` the point doubled).
- Decide protrusion deliberately — sink a flat marking slightly in, push a
  rounded eye out by a fraction of its own radius.
- When a part is missing, rule out occlusion before existence: flip the parent's
  material to `wireframe`, or read the child's world position and compare it
  against the surface, rather than hunting the scene graph.
- The same applies to decals on any closed primitive, not just ellipsoids.
