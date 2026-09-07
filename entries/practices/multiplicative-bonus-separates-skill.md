---
title: An affine per-unit reward barely separates skill levels; a compounding one does
tags: [game-design, balance, simulation]
added: 2026-09-07
---

## Fact

A reward shaped `base * (k + m*quality)` is affine in quality, so the ratio
between a flawless unit and a merely good one is bounded and usually small. At
`0.35 + 0.85q`, quality 1.0 pays 1.20 and quality 0.85 pays 1.07 — a 12% edge
for the difference between perfect and good.

When the failure condition is a fixed cost growing against a capped throughput,
that 12% buys almost no extra survival: expert and competent play die at nearly
the same point, and the run length stops reporting skill.

A multiplier that compounds across consecutive successes fixes the top end
without touching the bottom, because only sustained quality reaches it. Measured
on one game with everything else held constant, adding a streak multiplier on
the tip (×1 to ×2 over ten clean units, reset by any lapse) moved median days
survived from 17 to 24 for a flawless bot and 15 to 20 for a good one — the gap
between them doubled.

## Why it matters

The flat top end is easy to misread as "the game is too hard" or "the ramp is
too steep", and both readings lead to changing the difficulty curve, which moves
every skill level together and leaves them just as indistinguishable.

It also shows up late: the levels separate fine early, when the cost is well
below the income ceiling, and converge only in the endgame where the score is
actually decided.

## How to apply

- Check the payout ratio between a perfect and a merely good unit before tuning
  anything else. If it is under about 1.2x, no amount of curve adjustment will
  separate them.
- Add the compounding term to the *discretionary* part of the reward (tips,
  bonus, combo), not the base, so a struggling player is not further punished.
- Reset it on any lapse and cap it, or it becomes the only thing that matters.
- Verify by isolation: toggle the multiplier alone, with cost and throughput
  fixed, and compare the *gap* between bots rather than either bot's absolute
  number.

Related: [[skill-meter-needs-escalation]], [[simulated-error-is-per-decision]].
