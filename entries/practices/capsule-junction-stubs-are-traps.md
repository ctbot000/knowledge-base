---
title: A capsule end that stops flush with the wall it joins leaves a notch that traps a body for good
tags: [game-design, collision, geometry]
added: 2026-09-10
---

## Fact

Collision worlds are commonly built from capsules — a segment plus a radius —
because one primitive covers walls, rails, guides and gates. Where two of them
meet, only one arrangement is safe: the joining capsule's endpoint must sit
*inside* the other's body.

An end that stops flush, or overshoots by even a few pixels, leaves a small
upward-facing shelf between the two surfaces. A body that lands there is pushed
by one surface into the other, and every individual resolution is correct, so it
never leaves. The same shape appears wherever a member crosses a wall and pokes
out the far side.

The related failure is a passage whose clearance is the sum of two radii plus
the body's diameter and comes out a fraction short. Nothing reports it: the
route is simply never taken, and the symptom is "the physics feels wrong over
there", several layers away from the arithmetic.

## Why it matters

Neither defect is visible in a screenshot, and neither is reachable by ordinary
play — a body has to arrive slowly and from one particular side. So they survive
manual testing and appear once, to somebody else, as a permanently stuck object.

Because the collision code is correct, the investigation goes to the resolver,
the timestep and tunnelling before it goes to the geometry.

## How to apply

- Bury the joint: end the joining capsule on the other's spine, not on its
  surface. Overlap is free; a stub is not.
- Order members by height where they cross: nothing may protrude above the
  surface a body slides along, or the protrusion becomes the shelf.
- Verify by sweep, not by eye. Release a body from a grid of positions across
  the whole world, step for tens of seconds, and assert every one resolves —
  drained, captured or still moving. Print the resting coordinates of the ones
  that do not; the trap's location falls straight out.
- Keep a last-resort recovery anyway: shake anything that has been stationary
  for several seconds, excluding states where being held is the intent.

Related: [[boundary-clamp-runs-after-collision]], [[forced-input-obstacle-fits-the-band]].
