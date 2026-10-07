---
title: A follower's no-progress check fires whenever its leader moves at the follower's own speed
tags: [simulation, game-design, ai, pathfinding]
added: 2026-10-07
---

## Fact

Declaring a follower lost (to teleport it, or path it afresh) when its
distance to its leader has not improved for N seconds assumes the leader
stands still. A follower keeping its gap behind a leader walking at its own
pace never closes that gap, so the check fires during perfectly good
following, at a rate set by how long the leader walks.

## Why it matters

The fallback meant for rare dead ends becomes routine: pets, companions and
escorts blink to their leader every few seconds of an ordinary walk. In a
simulated run it shows as a steady count of "lost" events on open, flat
ground, where nothing could be in the way, and tuning N only changes the rate.

## How to apply

- Run the no-progress timer only while the leader is stationary (still for
  half a second, say); a follower that cannot reach a waiting leader is the
  case it exists for.
- For the moving case use a separate stuck test: wanting to move but
  covering a small fraction of the expected distance.
- Count the fallback's firings per kind of reason in a long simulated run on
  open ground: anything above zero there is the check, not the terrain.
