---
title: Ink lines can come from the depth buffer alone, because 1/z is affine across every plane
tags: [graphics, shaders, post-processing, npr]
added: 2026-11-21
sources:
  - https://www.songho.ca/opengl/gl_projectionmatrix.html
---

## Fact

Under a perspective projection, the reciprocal of view-space depth (and the
raw depth-buffer value, which is affine in it) varies *linearly* across the
screen over any flat surface, whatever its slope. So in a post pass, the second
difference of 1/z between a pixel and its neighbours, divided by its own 1/z,
is zero on every plane and non-zero only where two faces meet (a crease) or one
thing stands in front of another (a silhouette, where z itself also jumps).
That is enough for cartoon outlines without a normal buffer.

## Why it matters

The usual depth-only outline tests the first difference of z, which also fires
on any surface seen at a grazing angle: ground running away from the camera
gets striped with lines that are not edges, and raising the threshold to hide
them drops real creases. Rendering a normal buffer to find creases instead
costs another pass over the scene, and custom shaders that do not write it come
out without lines.

## How to apply

- Silhouettes: `max |z_neighbour - z| / min(z...)` over the four neighbours,
  past a few percent.
- Creases: `(|1/zL + 1/zR - 2/z| + |1/zD + 1/zU - 2/z|) / (1/z)`, past a few
  percent.
- Make the crease threshold grow with distance (times `1 + z/25` or so) and fade
  lines out towards the fog, or gentle bends far off turn into noise.
- Do it on linear (not tone-mapped) colour before the output pass, darkening the
  colour rather than painting black, and run an FXAA pass after: the lines are
  one or two pixels and alias otherwise.
