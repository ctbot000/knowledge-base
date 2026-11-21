---
title: A vertex where a surface's two sides meet gets a zero normal from three.js computeVertexNormals, which draws black
tags: [threejs, webgl, geometry, normals]
added: 2026-11-22
sources:
  - https://github.com/mrdoob/three.js/blob/dev/src/core/BufferGeometry.js
  - https://registry.khronos.org/OpenGL-Refpages/es3.0/html/normalize.xhtml
---

## Fact

`BufferGeometry.computeVertexNormals()` sums the normals of the faces round
each shared vertex and then normalizes with `Vector3.normalize()`, which
divides by `length() || 1`: a sum of exactly zero stays `(0, 0, 0)`. The
material's fragment shader does `normalize(vNormal)`, which GLSL leaves
undefined for a zero vector; GPUs return NaN, the lighting goes NaN, and the
pixels draw black.

## Why it matters

The sum is zero wherever faces with opposite normals meet in equal measure at
one vertex: both sides of a one-cell-thick wall in surface nets or marching
cubes (an ambiguous, checkerboard cell), a fold back onto itself, a sheet
whose two sides were welded. On a voxel wall that runs straight up, the bad
vertex repeats every layer and shows as a thin black stripe down a smooth
model, which looks like a texture or lighting fault, not a geometry one. A
blur or bloom pass after it can spread the NaN further.

## How to apply

- After `computeVertexNormals()`, scan the normal attribute for vectors of
  length ~0 and replace each: with its triangle's own face normal when the
  mesh is expanded to one vertex per corner, or with the average of the
  faces on one side when it stays indexed.
- Debugging: a black line or stripe on a smoothly shaded procedural mesh
  that stays put on the model whatever the light does is the first thing to
  check this way.
