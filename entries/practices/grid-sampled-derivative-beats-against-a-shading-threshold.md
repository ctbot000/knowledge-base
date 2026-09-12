---
title: A shading rule keyed on a grid-sampled slope renders narrow features as a row of teeth
tags: [graphics, terrain, rendering, debugging]
added: 2026-09-12
---

## Fact

Height fields are commonly shaded by rules that are steep functions of slope —
snow does not settle on a steep face, exposed rock reads darker. Slope is
sampled per vertex from neighbouring heights, so it carries the grid's
resolution.

Where a narrow feature crosses the grid at an angle — a cut bank, a ridge, a
crack — its phase against the grid changes along its length. A linear use of
that slope hides it. A steep `smoothstep` amplifies it into a regular row of
teeth marching along the feature.

The tell is that **the geometry and the normals are perfectly smooth and the
colour is not**. Rendering the same mesh with a normal-visualising material
shows nothing wrong; the artifact lives only where a threshold was applied.

## Why it matters

Teeth look like a mesh problem, so the search starts at resolution,
triangulation and `computeVertexNormals` — all of which are innocent, and none
of which fix it. Raising the mesh resolution makes the teeth smaller and more
numerous, which reads as progress and is not.

## How to apply

- Split the two uses of slope. Keep the raw per-vertex slope for anything
  linear; low-pass a copy — one 3x3 average over the grid neighbours is enough —
  for anything that goes through a threshold.
- Widen the threshold band while you are there. A rule that switches over a
  narrow range of slope will find whatever high-frequency content exists.
- To confirm the diagnosis in one step, swap the material for a normal-space one.
  Smooth normals with teeth in the shaded render means the fault is in the
  colour, not the mesh.
