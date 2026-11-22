---
title: A voxel world can be drawn as smooth land by joining columns one step apart and splitting the rest, with what stands on it lifted onto the skin as it is drawn
tags: [terrain, voxel, graphics, procedural-generation]
added: 2026-11-18
updated: 2026-11-22
---

## Fact

Keep the voxel world for movement and rules, and draw its ground as one mesh
over the column tops: points on a half-cell grid, one vertex per group of
columns that meet at the point and are *joined* (heights differ by at most the
step a character can climb), each vertex the weighted average of the joined
columns within about 1.6 cells. Columns further apart are split: each side
keeps its own edge vertices and a vertical strip of rock between them closes
the gap, pushed about by noise of position so shared vertices stay shared.
Under water, join everything. Then draw anything standing on the ground at
`surface(x, z) + (y - support)`, where `support` is the top of the highest
column under its footprint at or below its feet, and put it back after
drawing.

## Why it matters

A blurred heightfield either buries characters at the foot of a cliff or floats
them at its top, by up to the cliff's height, and turns impassable steps into
slopes that look walkable. The join rule makes slopes exactly where walking
goes up and faces exactly where it cannot, so the drawn surface stays within
about half a cell of what is walked on.

## How to apply

- A step up needs no smoothing of its own if the feet go up the cell at
  once: `support` jumps with them, so the drawn height stays continuous. A
  jump arc or a fall off a step shows through, so movement has to walk the
  steps as slopes (see
  [voxel-steps-under-a-smooth-skin-are-walked-as-slopes](voxel-steps-under-a-smooth-skin-are-walked-as-slopes.md)).
- Bake ambient occlusion from the column heights, and lamp light from the
  game's own light grid, into vertex attributes.
- Keep the lift out of picking and physics; it is a drawing offset only.
