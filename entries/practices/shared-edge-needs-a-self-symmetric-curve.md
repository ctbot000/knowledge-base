---
title: Two shapes sharing an edge must trace one curve, and only a self-symmetric one reverses by a sign flip
tags: [geometry, graphics, procedural-generation]
added: 2026-09-07
---

## Fact

When two tiles share a boundary, each draws it in the opposite direction and
with the opposite outward normal. The two outlines coincide only if one curve,
traced backwards, lands on exactly the same points.

If the boundary's shape is defined symmetrically about its own midpoint, that
reversal is a pure parameter flip — negate the side it bulges towards and negate
its offset along the edge, and the second tile reproduces the first tile's curve
exactly. Introduce any asymmetry (a feature nearer one end, a wider flank on one
side) and the flip no longer maps the shape onto itself.

## Why it matters

The failure is sub-pixel and looks like a rendering artifact: a hairline of
background between two tiles that are supposed to interlock, or a faint doubled
edge where they overlap. It survives snapping the shapes to exact positions,
because the positions were never wrong.

It also shows up late. A boundary generator usually starts symmetric, and the
asymmetry arrives with a later "add some variation" change, which then appears
to have broken placement rather than shape.

## How to apply

- Define the shared feature about the edge midpoint and vary it only with
  parameters that preserve that symmetry — size, depth, a mirrored pair of
  control points.
- To vary its position along the edge, keep the offset as an explicit signed
  parameter so the reverse traversal can negate it, instead of baking it into
  the point list.
- Assert it rather than eyeballing it: sample the curve forwards from one tile
  and backwards from its neighbour and compare the point lists. Symmetry means
  point `i` and point `n-1-i` mirror, which is a cheap unit test.
- The same rule covers procedural terrain and mesh chunk seams, not only tiling
  and puzzle cuts.
