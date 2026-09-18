---
title: A radial kernel sized in pixels is an ellipse in grid terms whenever the cells are not square
tags: [graphics, canvas, layout]
added: 2026-09-19
---

## Fact

Spreading a value over a grid — a heat map, a sensor simulation, a brush, a
falloff around a hit — is normally written as a radial kernel in pixel space:

```js
const sigma = 1.2 * Math.min(cellW, cellH);
v = amp * Math.exp(-((nx - px) ** 2 + (ny - py) ** 2) / (2 * sigma * sigma));
```

That is round on screen and therefore *not* round in cells. With `cellW` twice
`cellH` it reaches twice as many rows as columns, and no single pixel sigma
fixes it: `min` starves the wide axis, `max` floods the narrow one. Evaluate
the distance in grid units instead:

```js
const sigN = 1.2;                       // in cells, not pixels
const fx = px / cellW - 0.5, fy = py / cellH - 0.5;
v = amp * Math.exp(-((col - fx) ** 2 + (row - fy) ** 2) / (2 * sigN * sigN));
```

## Why it matters

The symptom points at the wrong file. Too few cells clear the threshold, so it
reads as a bad threshold or a weak amplitude, and the resulting centroid,
count or classification is quietly derived from a sliver two cells wide.

It also only appears at some sizes. A container that happens to be near the
grid's own aspect ratio makes the cells square and the bug invisible, and it
returns at the next breakpoint or on the next screen.

## How to apply

- Decide which space the quantity lives in. A fingertip covers a fixed number
  of electrodes, not of pixels, so the kernel is specified in cells; write it
  in that space and convert the pointer into it once.
- Assert it: place the source at a cell centre and check that the count above
  threshold is the same when the grid is stretched to a different aspect.
