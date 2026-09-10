---
title: A collision world's segment list is not a display representation, and drawing it one primitive per segment shows the joins
tags: [graphics, game-design, geometry]
added: 2026-09-10
---

## Fact

Physics stores walls as independent segments, because that is what a collision
test wants: each one is checked on its own and neighbours never interact. A
renderer handed the same list will happily draw one rounded box, capsule or
extrusion per segment — and every rounded end then protrudes through the
neighbour it was supposed to continue into.

On a straight run nothing shows. On a curve, each segment's cap pokes out at a
slightly different angle, and a smooth wall renders as a scalloped, ribbed one.
The tell is that the artefact tracks curvature: worst where the polyline turns
fastest, invisible where it is straight.

## Why it matters

The geometry is right, the collision is right, and the mesh builder is right —
so the ribbing reads as a bug in the primitive, and gets chased in its cap
tessellation or its radius. The defect is upstream of all of that: the display
needs an object the physics representation does not contain.

The same shape appears wherever a simulation's data structure is drawn
directly — a navmesh drawn per triangle, a path drawn per waypoint, a heightmap
drawn per cell.

## How to apply

- Recover the polylines first: chain segments whose endpoints coincide within a
  tolerance, in either direction, then extrude each chain as one mitred rail
  with a shared cross-section. Cap the miter length so a sharp corner does not
  produce a spike.
- A pass over a few dozen segments is O(n²) and runs once at load; do not
  complicate it.
- Assert the chaining rather than eyeballing it: every segment must land in
  exactly one chain, and the total should be `segments x per-segment + chains x
  per-cap`. A silent failure to chain just puts the ribbing back.
- Round cross-sections are the exception — overlapping spheres along a tube
  read as continuous, so wire guides can stay per-segment.
