---
title: Anything a level builder works out from the terrain when it places a thing is wrong once more terrain is built after it
tags: [procedural-generation, game-design, levels, testing]
added: 2026-11-28
---

## Fact

When a builder computes an entity's derived data at the moment it is placed — a
patrol's end points from the ledge it stands on, a turret's range to the next
wall, a spawn's support — the answer reflects only the terrain built so far.
Steps, blocks or walls added afterwards, often a line later in the same section,
are inside the range it already settled on.

## Why it matters

The level reads correctly and every piece of code is right; the entity simply
walks into a step or shoots through a wall that was not there when it asked. The
bug depends on the order of lines in the level script, so moving one call fixes
or causes it, and it only shows when the entity reaches that end of its range.

## How to apply

- Place entities with their raw parameters only, and derive everything that
  depends on the terrain in one pass after the whole level is built.
- Test it the way it fails: sample each moving entity over a long stretch of
  time and assert its box never overlaps solid terrain.
