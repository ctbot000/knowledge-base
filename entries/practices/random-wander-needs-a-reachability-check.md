---
title: An agent that wanders to random targets stays in any nook unless each target is checked for a way there when picked
tags: [game-design, ai, voxel]
added: 2026-10-04
---

## Fact

"Pick a random point nearby, walk to it, re-pick when stuck" works in the open
and fails in a nook: when almost every candidate is unreachable, re-picking
just draws another unreachable one. Validating the straight way to a
candidate when it is picked — the body's whole footprint fits at every sample,
no step up or down bigger than it can take, no water it avoids — fixes it.

## Why it matters

Agents spend whole sessions walking on the spot by a wall or a cliff, which
reads as a movement or collision bug. In one voxel world only 0.14% of
directions out of such a nook were clear; most rejections came from the
check itself.

## How to apply

- Sample the line from the agent to the candidate every half cell, and accept
  the candidate only if every sample passes the same rules the mover obeys.
- At a step, sample the footprint at the height the mover will reach: with
  the centre still over the low cell, the box already overlaps the high one,
  and the mover hops up there. Rejecting that sample made almost every way
  "blocked" (0.14% clear; 14% once the hop was allowed).
- Count deep water the agent swims through as passable by the water column,
  not by a ground height under it, which a downward scan never reaches.
- Keep the stuck detector as a backstop, and stop the agent at edges it could
  not climb back over, or it walks off a ledge into a pit it cannot leave.
