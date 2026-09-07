---
title: A steeper entry angle widens the target, so the best shot is the one that leaves the frame
tags: [game-design, balance, camera]
added: 2026-09-07
---

## Fact

A projectile passing through a horizontal opening sees an effective opening of
roughly the true width times the sine of its entry angle. Steeper arcs therefore
have a genuinely wider tolerance and are the objectively better shot — this is
physics, not a tuning choice.

A steeper arc is also a taller one. On a fixed camera, the trajectory with the
widest scoring window is the one that exits the top of the view: measuring the
apex of every scoring shot, the widest windows sat at 66-77° with apexes well
above the frame, and about a quarter of all scoring shots left the view entirely.

## Why it matters

The game rewards the shot the player cannot watch, which reads as a camera bug
rather than as a consequence of the scoring geometry. Each obvious remedy costs
something real:

- Zooming out shrinks the target and everything else with it.
- Adding a ceiling reintroduces rebounds that
  [rescue overshoot](reflecting-boundary-rescues-overshoot.md).
- Capping launch speed does bound the arc height, but it bounds range too, and
  can put the longest shot out of reach even at its optimal angle.

## How to apply

- Measure the apex of scoring trajectories, not just whether they scored. "Does
  it go in" and "can it be seen" are separate assertions.
- Prefer tracking the projectile past the edge — an indicator pinned to the
  frame — over constraining the physics to keep it inside.
- Before capping launch speed, check the longest shot is still reachable at its
  minimum-speed angle: `v_min^2 = g * (dy + hypot(dx, dy))`.
