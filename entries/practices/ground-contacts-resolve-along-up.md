---
title: A character pushed out of walkable ground along the contact normal crawls uphill and stops at low rims
tags: [physics, character-controller, games]
added: 2026-11-25
---

## Fact

If every contact is resolved alike (push out along its normal, remove the velocity
into it) and the vertical part of the velocity is then dropped because the character
is on the ground, each substep keeps only cos² of the slope angle of the forward
speed. The loss repeats every substep, so it does not cost a share of the speed: the
character settles at the crawl where one substep's acceleration equals it, about half
a metre per second on a 45° incline whatever the running speed.

## Why it matters

Flat ground and walls both behave perfectly, so it passes every obvious test. In play
bumps feel like mud, and the rounded rim of a step or a pressure pad holds a running
player for a second or more, or for good when the rim is steeper. Auto-hop hides part
of it, for walkers more than for runners.

## How to apply

- Split contacts by slope. Walkable ones (normal within the slope limit of up): move
  straight up by `penetration / dot(n, up)` and cancel only downward velocity. The
  rest: push out along the normal as before.
- Step up low ledges separately: when blocked by a wall, test the foot sphere raised by
  the step height and a little forward; if it is free, rise by the gap that is left.
- Make "ground" and "wall" one threshold with no gap between them, or contacts in the
  gap are neither and nothing climbs them.
- Test with numbers: average speed of a straight run over every piece of ground, and
  walking on to each low platform from eight sides with and without auto-hop.
