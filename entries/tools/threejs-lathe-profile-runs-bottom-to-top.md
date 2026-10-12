---
title: A three.js LatheGeometry faces outward only when its profile points run from bottom to top
tags: [three.js, graphics, geometry, winding]
added: 2026-10-12
sources:
  - https://threejs.org/docs/#api/en/geometries/LatheGeometry
  - https://github.com/mrdoob/three.js/blob/dev/src/geometries/LatheGeometry.js
---

## Fact

`LatheGeometry` winds its triangles from the order of the profile points it is
given. Points listed with y increasing (bottom to top) give outward-facing
triangles; the same points listed top to bottom give a surface wound inside
out. The documentation only says each x must be positive, so nothing warns
about the order. Checked on r186: a four-point profile gave 48 outward faces
one way round and 48 inward the other.

## Why it matters

The two cases fail differently, which hides the cause. A closed profile (one
that starts and ends on the axis) wound inside out still looks solid with
front-face culling: the near wall is culled and the far wall's inner side now
faces the camera, so you see a plausible shape with slightly wrong lighting.
An open profile (a sleeve, a cuff, a cup) has no far wall to stand in for it
and simply vanishes from outside, leaving only whatever decorates its edge.
Shapes that hang from a joint, such as limbs written from the shoulder down,
are the usual way to get the order backwards.

## How to apply

- Write every lathe profile from its lowest point up, or reverse it at the call
  site: `new LatheGeometry([...points].reverse())` for a top-down list.
- Test a new lathe the cheap way: for each triangle, the cross product of two
  edges should point away from the y axis (dot it with the face centre's
  horizontal offset).
- If an open lathe is missing but its rim decoration shows, suspect point order
  before materials or culling settings.
