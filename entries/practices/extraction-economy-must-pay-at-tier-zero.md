---
title: An extraction economy must be net-positive with the starting loadout
tags: [game-design, balance, simulation]
added: 2026-09-08
---

## Fact

In a gather-sell-upgrade loop, the per-trip consumables — fuel, repairs,
ammunition, tolls — are paid at full price from the first minute, while yield is
gated behind the upgrades those payments are supposed to fund.

If one trip with tier-zero equipment costs more than it earns, the loop runs
backwards. The player converges on zero, and every mechanic that exists to
rescue them (a cheap tow, a partial refill, a free respawn) keeps them alive
inside the spiral rather than out of it.

The margin is easy to get wrong because the endgame numbers look healthy: the
same world can pay 30x per unit dug at depth and 0.8x at the surface.

## Why it matters

The symptom is not "the economy is unbalanced". It is a player, or an automated
playtester, that appears **stuck**: barely moving, barely earning, repeating
short trips. That reads as a pathing bug, an AI bug, or a level problem, and the
investigation goes anywhere except the price of fuel.

It is also invisible to anyone testing from a mid-game save, which is how a
designer tests once the early game feels finished.

## How to apply

- Compute the tier-zero trip explicitly: expected yield per unit of effort,
  minus consumables at list price. Require a clear surplus — roughly 3-5x, not
  1.1x — because early players are inefficient.
- Measure yield along the path actually travelled, not as a density over the
  whole map. A one-cell-wide shaft samples far fewer cells than the map average
  suggests, and travel through open space collects nothing.
- Re-check tier zero after every change to consumable pricing or costs. It is
  the one configuration nobody plays again after the first ten minutes.
