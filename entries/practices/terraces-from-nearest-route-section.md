---
title: Terraces keyed to the nearest stretch of the route make gated progression hold by construction
tags: [game-design, level-design, voxel, procedural-generation]
added: 2026-11-07
---

## Fact

To gate a linear route through a block world (a walker climbs one block at a
time and drops any height), number the route's stretches between gates in
order and give every column the height `base + lift × n`, where `n` is the
number of the route stretch nearest that column. Every patch of land then
belongs to exactly one stretch; wherever two patches meet there is a cliff
`lift × Δn` high, never a slope; and the only link from one stretch to the next
is the route itself, climbing as a ramp (cut into the higher terrace, a
causeway over the lower), with the gate on it.

## Why it matters

Hand-placed terrain (rings round a peak, bands across the map, "bulges" where
camps need room) leaks wherever a band is narrower than what stands on it or
two bands meet at an edge, and each map needs its own repairs. The nearest-
stretch rule has no such places: new maps hold their gates on the first try
over hundreds of seeds, and the route can wind anywhere.

## How to apply

- Sample the route densely; give each ramp segment's first half the lower
  number and its second half the higher, so the boundary falls mid-ramp, and
  put the gate there, spanning wider than the cut.
- Number in climbing order. A later area higher than every earlier one cannot
  be dropped into, which is the leak height-agnostic rules miss.
- Do not fade the lift towards the coast: a shore where every terrace tapers to
  sea level is one beach that climbs into all of them. Let terraces drop sheer
  into the sea, and keep one low beach where swimmers can climb out.
- Keep `lift` well above the terrain's own noise (4-5 blocks for a walker that
  climbs one) so noise never closes a cliff into a step.
- Still verify with a step-aware flood fill over many seeds, gate by gate.
