---
title: Scattering points with `i * stride % size` lays them on a lattice, not at random
tags: [graphics, procedural-generation, randomness, texture]
added: 2026-09-09
---

## Fact

`x = (i * stride) % size` is the usual way to place "random-looking" points
without an RNG, and it is not random in the way it looks. Consecutive samples
differ by exactly `stride % size`, so the points walk one straight line that
wraps — they land on a small family of parallel lines. Doing it independently
per axis gives a 2D lattice.

Sand grains placed at `x = i*137.51 % 142`, `y = i*71.31 % 120` step by
`(-4.49, +71.31)` every iteration, so at 900 grains the bunker is covered in
diagonal chains rather than grain.

The structure hides at low counts and emerges as density rises, which is exactly
backwards from how it gets tested: a handful of points to check the code, then
the real count in the render.

## Why it matters

This trick is reached for precisely where randomness must not be *visible* —
texture grain, speckle, stars, scattered foliage, dither. It is also the form
that reviews as fine: deterministic, no seed to thread, no RNG to import.

The failure appears only in the rendered image, and it reads as a texture or UV
problem — repeating diagonals look like a tiling artifact — so the search starts
in the sampler and not in the six characters that chose the stride.

## How to apply

- Use the R2 low-discrepancy sequence instead. It is the 2D golden ratio, one
  multiply per axis, and it fills the square without a lattice:

  ```js
  const x = ((i + 1) * 0.7548776662466927 % 1) * width;
  const y = ((i + 1) * 0.5698402909980532 % 1) * height;
  ```

- For grain, prefer low-discrepancy over a plain RNG anyway: uniform random
  clumps and leaves holes, which reads as blotchiness rather than as texture.
- The tell is the sample count. Raise it tenfold: true scatter only gets denser,
  a lattice gets more obviously ruled.
- A hash of `i` works too, but only a decent one — the low bits of `i * k` are
  the same lattice by another name.
