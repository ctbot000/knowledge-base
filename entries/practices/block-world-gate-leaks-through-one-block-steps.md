---
title: A gate in a block world only holds if nothing beside it makes a one-block step
tags: [game-design, level-design, voxel, procedural-generation, testing]
added: 2026-11-03
---

## Fact

In a voxel world where a walker climbs one block at a time and drops any
height, a barrier across a path is only a barrier if every way round it is
at least two blocks sheer. Almost every decoration that looks harmless makes
the staircase that gets round it: the eased shoulders beside a graded path,
the slope a level platform is blended into, a tree crown standing at the foot
of a cliff or reaching over a river, a railing or lamp post beside a gate, a
wall built a fixed height over a slope (its uphill side is one step), a
diagonal line of blocks the path crosses at a bend, and any cliff you can
simply drop down from into a later area.

## Why it matters

The leak never shows in the intended walk, only in a search, and it depends
on the generator's seed: a map that holds for the seed you looked at leaks on
a third of the others (noise moves a cliff edge next to a ramp, a tree lands
by a wall). Players find the way round, and the progression the gates exist
for quietly stops existing.

## How to apply

- Verify with a step-aware flood fill from the spawn (stand on solid ground
  with headroom, up at most one block, any drop down, no water or lava), and
  assert which goals are reachable with each gate shut and after each opens.
- Run it over many seeds, not one; a sweep of ~150 found leaks two seeds hid.
- Put a gate where both sides of it are sheer: mid-bridge rather than at the
  bank, inside a cut deep enough (2+ blocks) on a straight stretch, never at a
  bend or where the ramp has nearly reached the top.
- Build cuts with no blend (sheer walls), keep tree crowns off water and off
  cliff feet, make walls high over the highest ground beside each column,
  and make gates taller than anything climbable next to them.
- Treat "can drop down into it" as a connection: a later area must not lie
  below an earlier one without a wall on the edge.
