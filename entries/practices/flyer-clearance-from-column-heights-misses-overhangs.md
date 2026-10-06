---
title: A flyer kept above the column heights it samples still flies into overhangs and the corners it never sampled
tags: [game-design, simulation, voxel, collision]
added: 2026-10-03
updated: 2026-10-06
---

## Fact

Terrain following in a block world usually keeps a flying agent a margin above
the highest block of the columns it samples: the one it is over and one ahead.
A column height cannot describe an overhang, and the step taken is not always
the step sampled, so the agent still ends up inside blocks:

- An eased step (slowing to land) or a diagonal that clips a column's corner
  ends in a column nobody sampled, below that column's top.
- A column entered from the side under its top (beneath a tree crown or a roof
  edge) is air there, so a solid-cell check lets the agent in; from inside,
  the height rule then sends it straight up through the overhang.
- The column it is landing in is exempt from the margin, so it gets entered
  from the side, under the very crown it means to land on.

The same hole opens on the ground: a keep-out rule (water, a safe zone, a
shelter) checked at one point ahead lets a body moving on a diagonal through a
corner cell that the point skips over.

## Why it matters

Each failure lasts a few frames, around one step in two thousand, so spot
checks pass, and a glimpse of a bird inside a hedge reads as a rendering
glitch rather than a movement rule.

## How to apply

- Gate every horizontal step on its real destination: refuse to move into a
  column below that column's top (or into a solid cell), and climb instead.
- Treat the landing column's top as the landing height itself, so it is only
  ever entered from above.
- Check ground paths too: every point of a hop or walk must be under open sky,
  not just its end, or the agent ends up under an overhang it cannot take off
  from.
- For a keep-out region, test the four corners of the body's footprint at the
  point ahead, not its middle: the footprint touches a corner cell before the
  middle can reach it.
- Measure it over long seeded runs on several worlds, counting steps whose body
  cell is solid, and drive the count to zero.

Related: [[spawn-time-constraints-do-not-survive-motion]].
