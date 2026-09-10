---
title: A wrongly wound triangle is not drawn inside out, it is not drawn at all
tags: [graphics, webgl, 3d]
added: 2026-09-11
---

## Fact

With back-face culling enabled, whether a triangle is drawn is decided by the
sign of its projected area — that is, by the order of its three vertices. A
triangle wound the wrong way is discarded before rasterisation. There is no
error, no warning, no z-fighting and no flipped shading. The geometry is not
there.

This is not the intuition the name suggests. "Back face" implies something that
would have been drawn facing away; what actually happens to a single-sided flat
object is that it disappears from one side and is perfectly normal from the
other.

## Why it matters

The symptom is a missing feature rather than a broken-looking one, so the
investigation starts in the wrong half of the program. A highlight that never
appears reads as "the state was never set", which sends you through the event
handlers, the uniforms and the code that decides when to show it — all of which
are correct.

It also fails selectively in a way that reinforces the wrong theory. Meshes
built by one helper appear while meshes from a sibling helper do not, because
their index orders happen to differ by one swap, so the bug looks like it
belongs to whatever those particular meshes represent.

## How to apply

- Assert winding where meshes are built, not where they are drawn. For every
  triangle, `cross(v1 - v0, v2 - v0)` must point along the face normal you
  intend. It is a pure function of the mesh, so it is cheap to test and it
  catches the fault at its source.
- Turn culling off for single-sided flat art — overlays, decals, ground quads,
  UI planes. There is no interior to hide, so culling buys nothing and risks
  losing the whole object.
- When something is *missing* rather than wrong, rule out culling first:
  disabling it for one frame distinguishes a geometry fault from a state fault
  in seconds.
- Remember that winding is relative: `frontFace` can be set to either CW or CCW,
  and a mesh that is correct in one renderer can vanish in another.
