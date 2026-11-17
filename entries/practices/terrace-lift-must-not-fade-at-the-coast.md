---
title: A terraced island that fades each terrace's lift toward the coast has a stair up every terrace along the shore
tags: [procedural-generation, level-design, terrain, game-design]
added: 2026-11-18
---

## Fact

A common way to raise terraces on an island is
`height = lerp(seabed, plateau + lift * tier, coastFade(edge))`. Inside the
coastal fringe every terrace then passes through the heights of the terrace
below it. Where two terraces meet at the shore, a walker that may climb one
step at a time walks down from the lower plateau onto the higher terrace's
fringe and climbs it, and along a wiggly coastline the fringe's heights change
gently enough to be a staircase. Every terrace gate can be walked round.

## Why it matters

The leak appears only on some seeds and only at the coast, so it reads as a
rare map bug rather than a property of the height function, and widening the
cliffs between terraces inland does nothing about it.

## How to apply

- Fade only the base land toward the sea bed; add the terrace's lift unfaded
  wherever the point is inside the coast: `lerp(seabed, base, fade) + lift *
  tier`, or a sheer step from sea bed to plateau for every terrace but the one
  meant to have a beach.
- Prove it with a reachability sweep over many seeds: from the start, a step up
  at a time and any drop down, which goal areas are reached before each gate
  opens.
