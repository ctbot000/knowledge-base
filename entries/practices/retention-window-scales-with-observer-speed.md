---
title: A retention window sized for a slow observer keeps stale entities in view when it moves fast
tags: [simulation, game-design, performance]
added: 2026-09-11
---

## Fact

Spawn and despawn radii are usually picked by looking at a still frame: how far
out should things appear, how far out should they be freed. Both are distances,
and neither says anything about how fast the observer crosses them.

Once the observer moves at a speed comparable to the window, the despawn radius
dominates. Entities spawned around an earlier position are not removed, so the
population the observer travels through is mostly the population it has already
left. In a scene where the camera descended at 11 m/s with a 30 m retention
radius, the entire set spawned near the surface was still resident 28 m above it,
three seconds later.

## Why it matters

The symptom is entities in a place they could not plausibly have swum, walked or
driven to — so it reads as a movement bug. The search goes into velocity
integration, steering and clamping, none of which is wrong; the entities never
moved at all, they were simply never freed.

It also quietly starves the region that is actually on screen, because the
population cap is already full of the stale set. Raising the cap makes the scene
denser *behind* the observer and no denser in front of it.

## How to apply

- Size the retention window in time, not distance: `radius ≈ spawnRadius +
  observerSpeed × secondsOfSlack`, with a second or two of slack.
- Keep despawn tight along the axis of travel and generous across it. A fast
  descent needs a small vertical window and can keep a wide horizontal one.
- When something is somewhere impossible, check whether it was ever removed
  before checking how it got there. Logging an entity's spawn position alongside
  its current one separates the two in one line.
