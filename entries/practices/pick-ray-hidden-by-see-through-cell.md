---
title: A pick ray that stops at the first non-empty cell cannot select an object standing inside a see-through cell
tags: [3d, game-design, input, voxel]
added: 2026-10-03
---

## Fact

Block-world pickers usually walk the ray through the grid, stop at the first
cell that is not air, then test entities and keep whichever is nearer. A
see-through cell, such as a flower or a tuft of grass drawn as crossed sprites,
counts as a hit, and its entry distance is nearer than anything standing inside
it, every time. A small animal in a flower, or a bee hovering at one, is drawn
in plain view and cannot be clicked: the flower takes the click.

## Why it matters

It looks intermittent. It depends on what happens to grow where the entity
stands, so it surfaces as a rare test flake or as "it sometimes ignores my
tap", while the entity's own hit volume tests fine in isolation.

## How to apply

- Let a see-through cell lose to an entity at about the same depth: prefer the
  entity when the hit cell is a sprite and the entity lies within a cell or so
  beyond its entry point.
- Do not extend that to solid cells; a wall must still hide what is behind it.
- Test with an entity placed inside a sprite cell on purpose, not on bare
  ground, so the case is deterministic rather than left to the terrain.

Related: [[perspective-aim-needs-a-cone]].
