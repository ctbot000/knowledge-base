---
title: Rounding a position after a grid check can move it into the neighbouring cell
tags: [game-design, voxel, networking, numerics]
added: 2026-11-26
---

## Fact

A point checked against a grid (free cell, on the ground, not in a wall) and
then rounded for storage or the wire is no longer the point that was checked:
`30.996` passes as cell 30 and is sent as `31.00`, inside cell 31. Any
quantisation — `toFixed`, hundredths as integers, half-floats — can push a
point that sat within one step of a cell edge across it.

## Why it matters

The failure is rare and position-dependent: most points are far from an edge,
so tests on a few seeds pass, and then an item spawns inside a wall, a body is
placed in solid ground and pops out, or two machines disagree about which cell
something is in. It looks like a bug in the check, which is correct.

## How to apply

Quantise first, then check the quantised value; or clamp the value inside the
cell it was checked in before rounding:

```js
const keep = (v) => +Math.min(Math.floor(v) + 0.98, Math.max(Math.floor(v) + 0.02, v)).toFixed(2);
```

The margin must exceed half the quantisation step (here 0.01). In a test, sweep
many seeds and assert the decoded value's cell, not the float's.
