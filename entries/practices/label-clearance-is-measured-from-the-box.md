---
title: An upright label clears a line by its support width and a vertex by its nearest corner, not by its centre's distance
tags: [geometry, graphics, svg, layout]
added: 2026-09-28
---

## Fact

For an axis-aligned label box w×h centred at c, the gap to a line through the
origin with unit normal n is |n·c| − ((w/2)|nₓ| + (h/2)|n_y|). The subtracted
term — the box's support along the normal — changes with the line's angle. The
gap to a point, such as a vertex with an arc drawn around it, is the distance to
the box's nearest corner or edge, up to √(w²+h²)/2 less than |c| on a diagonal.

## Why it matters

A label put "d from the vertex along the bisector" with d judged from its centre
looks right when the bisector is horizontal or vertical and overlaps on the
diagonals, so hand-checked layouts pass and random geometry does not. The needed
distance also grows as 1/sin(half-angle): a narrow angle pushes its label past
the arm ends and out of a figure that was fitted without it.

## How to apply

- On a bisector of half-angle α, place the centre at
  d = max over both sides of (support(n_side) + gap) / sin α.
- Then step d outward until the nearest-point distance to the vertex clears the
  arc radius plus a gap.
- Size the box from the tallest glyph actually rendered (a large "?" has a taller
  line box than digits); measure it with getBBox once instead of guessing.
- Include the label's box when fitting the figure to its viewport.
- Assert it over thousands of random figures: segment-vs-box (Liang–Barsky) for
  every line, nearest-point distance for arcs, box overlap between labels.

Related: [[svg-paint-order-hides-content]].
