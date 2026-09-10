---
title: Comparing normals to an axis mis-reports winding; the signed volume of a closed mesh does not
tags: [3d, graphics, geometry, procedural-generation]
added: 2026-09-11
---

## Fact

The obvious check for "are my faces wound outwards" — take each face's centroid,
take its normal, and see whether they point the same way from the model's axis —
is not a test. It is only valid for a star-shaped hull, and almost no real mesh
is one. Eyeballs, fins, jaws and any other part attached off-axis are *correctly*
oriented while pointing back toward the axis, so they read as failures.

On a procedurally built fish that heuristic reported 70% of faces inverted when
the only genuinely inverted surface was the body loft.

The signed volume is exact and needs no assumptions:

```js
let v = 0;
for (const [a, b, c] of triangles) v += dot(a, cross(b, c)) / 6;
// closed mesh, outward winding  =>  v > 0
```

It is one pass, it has no tuning, and it gives one number per mesh.

## Why it matters

A wrong-way mesh is invisible until it is rendered with backface culling, and
then it looks hollow rather than broken — which sends the search into the
shading, the normals or the light rig instead of the vertex order. Meanwhile the
heuristic that was supposed to catch it is producing a large, meaningless failure
count that hides the one real inversion inside it.

## How to apply

- Assert `signedVolume(mesh) > 0` per closed mesh in a build-time check. Run it
  on every primitive builder, not just the finished model.
- Open surfaces (a ground sheet, an unclosed hull) have no meaningful signed
  volume; check those by asserting the sign of the normal component you expect —
  every seabed face has `n.y > 0`.
- Double-sided geometry sums to exactly zero. Treat `v == 0` as "not closed",
  not as a failure.
- When the volume is negative, look at the *sequence* direction first: a loft
  helper that stitches ring `i` to ring `i+1` bakes in an assumption about which
  way the rings advance, and handing it a reversed chain flips every face while
  each individual ring still looks right.
