---
title: Camera-relative input on a vehicle bound to a looping track turns "forward" into "brake" once the track heads back
tags: [game-design, input, camera]
added: 2026-10-24
---

## Fact

When a vehicle can only move along a track (rails, a coaster, a lane) and
the player's stick or keys are read relative to a fixed camera, then
projected onto the track, "forward" means "along the track" only while the
track points away from the camera. Once a loop turns the track back towards
the camera, the same held key projects onto the reverse direction and acts
as a brake.

## Why it matters

The player holds forward the whole time and the car stops on the far side
of the loop, or rocks back and forth at the bottom of a dip. Every piece is
correct on its own (the input mapping, the projection, the physics), so it
reads as a speed or friction bug, and a simulation that pushes "the way the
car is going" never shows it.

## How to apply

- While the vehicle moves along the track, ease the camera yaw round behind
  its direction of travel (a few times a second, wrapping the angle), so
  camera-forward and track-forward stay within 90° of each other.
- Or read the input as track-relative (forward = along the heading) while
  on the track, whatever the camera does.
- Test it the way a player plays: hold one key through a whole lap in the
  real input path, not with input synthesized along the heading.
