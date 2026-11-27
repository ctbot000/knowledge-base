---
title: A tile platformer's "what is under me" by the body's centre column finds nothing for a body standing on a ledge's edge
tags: [game-design, platformer, collision, tiles, testing]
added: 2026-11-28
---

## Fact

A box standing on tiles is supported by any column its feet overlap, but its
centre can be over empty air: a body landing just onto a ledge rests with most
of its width over the gap. Any lookup of "the ledge (or tile) under it" by the
centre column alone then returns nothing for a body the physics holds up.

## Why it matters

The collision code is right and keeps the body standing, so the mismatch only
shows where something else asks where it stands: a reachability solver discards
the landing as a fall and reports a playable level as impossible, an AI thinks it
is airborne, a checkpoint or "standing on X" trigger never fires at the edge.
Long jumps land near edges more often than anything else, so the failures
cluster on exactly the hardest gaps.

## How to apply

- Look up the support the way the collision does: the columns under the box's
  feet, a hair in from each side (`floor(x ± (w/2 - ε))`), centre first.
- In a solver, assert on a known edge landing (the body's centre over the gap)
  before trusting a "not reachable" result.
