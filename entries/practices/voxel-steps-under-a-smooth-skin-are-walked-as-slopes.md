---
title: Under a smooth skin, a voxel world's one-cell steps must be walked as slopes, or moving feels like hopping over invisible bricks
tags: [terrain, voxel, physics, game-feel]
added: 2026-11-22
---

## Fact

When voxel ground is drawn as one smooth surface but movement still runs on
the voxels, the usual step handling (an auto-jump onto a one-cell ledge, a
free fall off one) shows through: on ground that looks evenly sloped, the
character stops, hops, drops, and the camera bobs with it. Movement has to
take the land's steps the way the skin draws them: up one cell at once, with
no jump and no loss of speed, and down a cell or two staying on the ground.

## Why it matters

Rolling voxel terrain is steps everywhere. Walking the paths of one
256-cell island gave a hop every ~14 m and a drop every ~23 m, about 7% of
walking speed lost to stalls, and players read it as "bricky" even where no
brick is drawn. A smooth renderer alone cannot hide it: the jump arc is real
motion, not a drawing offset.

## How to apply

- In the physics substep, when a horizontal sweep is blocked by a one-cell
  step of terrain with room above, put the feet on top and sweep again,
  keeping the velocity. After moving, if the footprint has lost its support
  and terrain lies one or two cells below with nothing in between, put the
  feet there. Only terrain to terrain: anything built is drawn as blocks, so
  it should still be hopped up and fallen off.
- Keep climbing at one cell; walking up two would change what is reachable.
- Draw at the surface height at the true position wherever the column under
  the centre is within the walked step of the supporting one; clamping into
  the support column turns each switch of support into a small jump.
- Networked copies: between two on-the-ground snapshots a whole-cell height
  change is a step. Switch the height where the support under the
  interpolated footprint changes; easing it floats the character up to a cell
  over the slope for a moment.
- See [smooth-skin-over-voxel-columns](smooth-skin-over-voxel-columns.md)
  for drawing the skin itself.
