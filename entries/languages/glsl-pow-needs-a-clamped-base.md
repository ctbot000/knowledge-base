---
title: GLSL pow() of a base a hair below zero is NaN, and one such pixel blanks rectangles of the frame once a bloom pass has blurred it
tags: [glsl, webgl, shaders, bloom, debugging]
added: 2026-11-25
sources:
  - https://registry.khronos.org/OpenGL-Refpages/es3.0/html/pow.xhtml
---

## Fact

`pow(x, y)` is undefined for `x < 0`, and GPUs commonly return NaN. Expressions
that cannot be negative on paper are in practice: `1.0 - abs(dot(n, v))` with two
unit vectors can come out as `-1e-7`, and an even power such as `pow(d, 2.0)` is
no safer, as it is not guaranteed to become `d * d`. A NaN written to a
half-float target survives every blur that samples it, so a bloom chain grows one
bad pixel into blocks as big as its coarsest mip.

## Why it matters

The symptom does not look like one bad pixel. Whole rectangles of the frame go
black, or transparent when alpha is NaN too, so a page shows whatever was behind
the canvas and `drawImage(canvas)` leaves the previous frame in place. It comes
and goes with the camera, and there is no GL error or console warning.

## How to apply

- Clamp the base at the call: `pow(max(0.0, x), k)`. Write squares as `x * x`.
- Re-normalise interpolated vectors before `dot`, and clamp a fresnel term:
  `1.0 - min(1.0, abs(dot(n, v)))`.
- Rectangular holes that appear with one new material: turn bloom off. If a speck
  remains where the holes were, it is a NaN in that material.
