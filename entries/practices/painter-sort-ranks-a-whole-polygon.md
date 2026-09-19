---
title: A painter's sort ranks a polygon by one depth, so a long surface is overpainted by the small things lying beside it
tags: [graphics, 3d, canvas]
added: 2026-09-19
---

## Fact

Depth sorting without a depth buffer gives each polygon a single number, usually
its centroid's distance. A 1400 m runway quad therefore sorts as though all of
it were 700 m away. Every terrain cell nearer than that is painted afterwards,
straight over the runway's near half.

Cutting the surface into strips fixes it, because each strip's centroid is then
close to the geometry it competes with. The strip length has to be comparable to
the neighbouring polygons, not merely smaller than the whole.

Coplanar surfaces need a second fix: paint on tarmac, tarmac on terrain, and a
level-of-detail ring overlapping its neighbour all sit at the same depth, and no
subdivision separates them. Bias the sort key instead — multiply the depth of
the layer that must win by slightly less than one.

## Why it matters

The symptom is that a large object is simply absent: it is transformed,
clipped, projected, coloured and queued, and every one of those steps is
correct. Nothing is logged, the polygon count is right, and the natural
suspicion falls on the projection or on culling.

## How to apply

- Emit large flat surfaces as strips sized like the terrain around them, not as
  one quad.
- Give every layer that is coplanar with another an explicit depth scale
  (`0.98` for the surface, `0.97` for the markings on it) rather than relying on
  insertion order — `Array.prototype.sort` is stable, but the order that reaches
  it is not meaningful.
- Assert the invariant in a test: after sorting, every item's depth is no
  greater than its predecessor's.
