---
title: A perfectly regular packing passes an impulse straight through instead of scattering
tags: [simulation, physics, game-design]
added: 2026-09-08
---

## Fact

Resolve collisions one pair at a time — the normal way — and a geometrically
exact packing behaves like a Newton's cradle. The impulse walks a single line of
centres and leaves at the far body; everything in between ends up back at rest.

A racked triangle of billiard balls struck square is the clearest case: 14 of the
15 finish within a few millimetres of where they started, while one crosses the
table. Every individual collision is correct, and the aggregate is nothing like
the real thing.

## Why it matters

It reads as an energy bug. The suspects that present themselves — restitution,
the impulse formula, the timestep, tunnelling — are all fine, and instrumenting
total momentum or the sum of speeds shows nothing wrong, because nothing *is*
wrong locally. The cause is symmetry: contacts that are exactly aligned, resolved
sequentially, never get a sideways component to split momentum with.

Real packings are never exact and real contacts are never purely normal, so the
effect has no counterpart to compare against outside the simulation.

## How to apply

- Perturb the initial state: a millimetre of jitter per body, comparable to the
  clearance between neighbours. Less than the clearance changes nothing.
- Model the off-normal part of a real contact. A tangential kick of a few percent
  of the normal impulse, in a random direction, is enough and is physical —
  friction between two surfaces does exactly this.
- Keep both deterministic. Draw from a stream seeded per event, not from the
  ambient generator, or the same inputs stop replaying to the same outcome.
- Diagnose by counting *how many* bodies moved, not how much energy remains. One
  fast body and a still crowd is the signature; a spread is what fixes look like.
