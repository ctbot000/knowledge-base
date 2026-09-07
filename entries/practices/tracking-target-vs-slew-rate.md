---
title: A moving target that outruns the thing chasing it fails a perfect player, not a bad one
tags: [game-design, control, balance]
added: 2026-09-07
---

## Fact

In any pursuit interaction — keep the needle in the drifting band, hold the
reticle on the mover — whether the task is possible at all is decided by two
speeds: the target's peak speed, and the **slew rate** of the thing the player
controls, meaning how fast the controlled variable can change under maximum
input. Where it rises and falls at different rates, the slower one binds.

If peak target speed exceeds that slew rate, the task is unreachable at its
worst moment however well it is played. For a target oscillating with amplitude
`A` and period `P`, peak speed is `2*pi*A/P` — so raising the amplitude or
shortening the period to "make it harder" crosses the line silently.

## Why it matters

It presents as tuning, not as a bug. A 100% failure rate reads as "too hard",
so the response is to soften the wrong dials — widen the tolerance, slow the
drain, extend the timer — none of which restores reachability.

It also hides from ordinary playtesting, because the *average* target speed is
comfortably trackable. Only the extremes of the cycle are impossible, and they
present as unlucky moments rather than as a structural limit.

## How to apply

- Keep peak target speed to roughly 30-70% of the slew rate. That headroom is
  what lets a player who has fallen behind catch up, which is where the skill
  actually lives.
- Assert it rather than eyeballing it: a test comparing the two constants costs
  nothing and pins the invariant against later tuning.
- Validate with a *flawless* simulated player. A perfect controller that still
  fails proves unreachability; a bad controller's failure rate cannot tell
  "impossible" from "hard".

Related: [[skill-meter-needs-escalation]], [[simulated-error-is-per-decision]].
