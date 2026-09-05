---
title: Overlapping translucent shapes compound per fill(), not per shape
tags: [canvas, graphics, frontend]
added: 2026-09-05
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fill
---

## Fact

With a translucent `fillStyle`, how many times you call `fill()` decides the
result, not how many shapes you drew.

Three overlapping circles added to one path and filled once produce a single
union at a uniform alpha — the overlaps are no darker than the edges. The same
three circles each given their own `beginPath()` and `fill()` composite over one
another, so every overlap lands at a higher alpha.

Sampling the pixels of `rgba(255,255,255,0.75)` puffs makes it exact: one path
gives alpha 191 everywhere; per-shape fills give 191 alone and 239 where two
overlap.

Winding is a separate matter and is not what causes this. Subpaths that share a
direction union cleanly under the nonzero rule, and `arc`/`ellipse` calls in one
path connect to the current point with an implicit line that falls inside the
shape — neither punches a hole.

## Why it matters

The two readings look identical in the code and different on screen, so the
choice is usually made by accident. Filling per shape gives blobs a bright core
and hard internal seams; filling once gives a flat silhouette. Whichever the
design wanted, it is a one-line difference that no amount of tweaking the alpha
will fix, because the alpha is not the variable.

It also bites the other way round: a "highlight" built from stacked translucent
strokes silently doubles up where they cross, and moving them into one path to
"clean up the code" erases the effect.

## How to apply

- Want a uniform silhouette: build every shape into one path, then `fill()` once.
- Want density where shapes overlap: `beginPath()` and `fill()` per shape.
- Deciding by measurement beats deciding by eye — `getImageData(x, y, 1, 1)[3]`
  reads the alpha at a point and settles it in seconds.
- `globalAlpha` multiplies each fill, so it scales the effect rather than
  removing it; it is not a way to flatten stacked fills.
