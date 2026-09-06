---
title: A stroke on a union path redraws the seams that a single fill erased
tags: [canvas, graphics, frontend]
added: 2026-09-06
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/stroke
---

## Fact

`fill()` and `stroke()` do not treat a path's subpaths the same way. Filling
composites the union of every subpath, so overlapping circles added to one path
come out as one flat silhouette. Stroking outlines each subpath individually —
including the ones buried inside the union — so the same path drawn with
`stroke()` shows a full circle around every shape, not the outline of the
combined form.

There is no fill rule that changes this. `nonzero` and `evenodd` decide which
regions are inside; stroking is not an inside/outside question at all.

## Why it matters

It bites immediately after doing the right thing. The way to get a blob with a
uniform edge is to build every shape into one path and fill once; adding a rim
or a highlight by calling `stroke()` on that same path then reinstates exactly
the internal seams the single fill was there to remove.

The result reads as a rendering artifact rather than as the outline that was
asked for, and the usual reflexes — lowering the alpha, changing the fill rule,
reordering the shapes — all leave it untouched, because none of them is the
variable.

## How to apply

- Fill the union path, then build a *separate* path holding only the silhouette
  you actually want outlined, and stroke that.
- When no such single shape exists, get the edge from a gradient fill or an
  inner shadow instead of a stroke; a radial gradient across the union gives
  depth with no seams.
- Deliberately stroking every subpath is a legitimate effect — a mesh, a wire
  drawing — and is the same call, so say which one you meant in a comment.
- The related fill-side trap is [overlapping translucent shapes compounding per
  `fill()`](canvas-translucent-fill-compounding.md).
