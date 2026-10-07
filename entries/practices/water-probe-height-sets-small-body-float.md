---
title: A fixed in-the-water probe height floats any body shorter than it at the probe, not at its own float line
tags: [simulation, physics, game-design, voxel]
added: 2026-10-07
---

## Fact

When a physics step decides "in the water" by sampling one point at a fixed
height over a body's feet, and buoyancy then holds a separate float line at
the surface, a body whose float line is below that probe can never rest on its
float line. Once its float line reaches the surface the probe is already out
of the water, so the body counts as out of it, gravity pulls it back, and it
hovers with the probe at the surface instead: deeper than designed, with its
float line always under water.

## Why it matters

Anything gated on "in the water, head out" never fires for such a body: the
kick that climbs out onto a bank, a surface stroke, a breathing check. Small
swimmers (pets, ducklings, small animals) paddle up to a one-block bank and
stay in the water for good. Floating looks right, so it reads as a bug in
stepping or climbing rather than in the probe.

## How to apply

- Make the probe height a per-body property, at or below the float line (half
  the float height works), and keep the old fixed value as the default so
  full-size bodies are unchanged.
- Test with the smallest body there is: it swims across a pond and climbs out
  onto a bank one block above the water, with no help.
