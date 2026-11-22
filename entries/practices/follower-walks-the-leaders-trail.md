---
title: A follower steered straight at its leader stalls at the first ledge or corner it went round
tags: [simulation, game-design, ai, pathfinding]
added: 2026-11-22
---

## Fact

A follower that steps toward its leader's current position meets every wall,
step too high and stretch of water the leader went round, and stops there.
The spots the leader stood on are a walkable route by construction, so record
them as breadcrumbs and walk them in order.

## Why it matters

On rough ground (voxel terrain, cliffs, coasts) a straight-line follower
stalls within seconds of leaving flat ground, and the rescue teleport meant
for rare dead ends fires constantly. Three details make breadcrumbs fail
almost as badly:

- Skipping every crumb within a radius, to avoid overshooting, cuts each
  corner by that radius, into the wall the leader walked round.
- Clearing the trail when the follower catches up discards the path between
  them, so it walks straight again once the leader moves on.
- A teleport to a spot "beside the leader" can land behind a wall or on a
  ledge it cannot leave.

## How to apply

- Drop a crumb when the leader has moved a fraction of a body length or
  changed height; keep a long trail.
- Move `min(step, distance)` to the next crumb and carry the rest of the
  step on to the one after; if a step is blocked, slide along the open axis.
- On catching up, keep the crumbs and drop only a loop that came back past
  the follower.
- When stuck for a second or two, teleport onto the trail a few units behind
  the leader, past the crumb it is stuck at; use "beside" only with no trail.
- Test by leading it over a real hilly route and asserting zero teleports.
