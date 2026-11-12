---
title: A guard against getting round a locked gate should flag where a barred goal can be reached from, not where open gates would lead
tags: [game-design, level-design, voxel, algorithms]
added: 2026-11-12
---

## Fact

"Ground reachable once every gate is open, minus ground reachable now" is not
the set of places a player must not be. Where movement has one-way edges (a
drop off a cliff), that difference also holds dead ends that are only entered
from later sections and lead nowhere. The exact set is backward reachability:
every place from which a still-barred goal can be reached with the gates as
they are.

## Why it matters

A runtime rule that sends a player back for being "past a gate" punishes
exploring when it uses the forward difference: swimming to a beach under a
cliff counts as cheating although nothing can be reached from it. On one
terraced map more than half of the forward difference was such dead-end ground.
The backward set never overlaps the legitimate area (a goal reachable from it
would not be barred), so it cannot fire on someone who is on the way.

## How to apply

- Build one successor function for the movement model (step up, drop, no
  water) and use it for both directions: flood forward from the start and
  the cleared checkpoints, then enumerate every standable cell's successors
  once to get reverse edges and flood backward from the goals the forward
  flood did not reach.
- Recompute when a gate opens or a checkpoint clears, not per tick.
- Test the ground under the body (the first solid within a few cells below),
  not the cell it occupies: a jumping or mounted player is rarely in a
  standing cell, so a dwell timer keyed on the occupied cell keeps resetting.
- Keep a short dwell time so a slip over an edge is not punished, and leave
  anything in neither set (water, rooftops, treetops) alone.
- Check per gate state, over many seeds: no cell in both sets, every barred
  goal has flagged ground around it.
