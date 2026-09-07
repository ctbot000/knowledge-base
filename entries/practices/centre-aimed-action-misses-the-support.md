---
title: A centre-aimed grid action deadlocks for an entity narrower than a cell
tags: [game-design, collision, simulation]
added: 2026-09-08
---

## Fact

Collision resolves against an entity's whole footprint, but a directional
action — dig, mine, attack, place, interact — is usually aimed from one point,
its centre:

```js
const tx = Math.floor((body.x + body.w / 2) / TILE);
const ty = Math.floor((body.y + body.h + 3) / TILE);   // the tile "below"
```

When the entity is narrower than a cell, its footprint can straddle two
columns. It then rests on the solid tile under one edge while the centre ray
points at the empty tile beside it. The action targets nothing, the support is
never removed, and the entity cannot move to change the situation.

The result is a hard deadlock in which holding the input does nothing at all,
indefinitely, with no error and no feedback.

## Why it matters

Every individual piece is correct — collision is right, the target lookup is
right, the input is read — so review finds nothing. The symptom (an agent that
stops making progress) points at pathfinding, at input handling, or at the
level, and the entity is standing still in a place where standing still is
plausible.

It is also position-dependent, so it reproduces only from certain offsets and
survives casual play testing.

## How to apply

- Aim the action at the **whole face** being pushed into, not at one ray: scan
  every cell the footprint spans on that side and take the first actionable one,
  preferring the cell nearest the centre.
- Snap the entity toward the cell it is acting on while the action runs, so the
  straddle resolves instead of persisting.
- Assert the invariant rather than eyeballing it: with the action input held and
  the entity supported, either the action target is non-null or the entity is
  moving. A headless run that holds one input for a minute finds this in
  seconds.
