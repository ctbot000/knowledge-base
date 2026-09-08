---
title: Simulated player error must be sampled per decision, not per tick
tags: [game-design, simulation, testing, balance]
added: 2026-09-06
updated: 2026-09-08
---

## Fact

Balance-testing a game with a deliberately bad bot only works if the noise model
matches the grain of the decisions. Applying a miss probability inside the
simulation loop does not model a bad player: at a 120Hz tick, a 35% chance of
skipping the action each tick just delays it by one tick — about 8ms — because
the next tick re-evaluates and acts. The survival curve stays flat no matter how
high the probability goes.

Measured on an endless runner, a 35% per-tick miss rate left a bot surviving
every run to the time cap. Moving the same idea to per-obstacle sampling —
one timing offset and one whiff roll drawn once per obstacle — produced a clean
gradient of median run lengths: 56s, 19s and 9s for ±30ms/1%, ±60ms/4% and
±100ms/10%.

## Why it matters

Both readings look like results and both are wrong in a specific direction. A
per-tick model reports that a punishing game is trivial, so the response is to
make it harder; a bot with no handicap at all reports that a fair game is
brutal, so the response is to make it easier. Either way the tuning moves away
from where it should be, and the simulation keeps agreeing with itself.

## How to apply

- Sample error once per decision the player actually makes — per obstacle, per
  shot, per turn — and hold that sample for the whole decision.
- Model timing as a continuous offset (a Gaussian on the trigger point), not as
  a dropped frame. Reaction error is early-or-late far more often than absent.
- Keep a separate, small whiff probability for decisions missed outright.
- Sanity-check the model before trusting the balance numbers: a perfect bot
  should never die on a fair game, and survival should fall monotonically as the
  noise rises. A flat curve means the handicap is not reaching the outcome.
- The rule governs **measurement** too, and there it under-reports: ticks in
  which nothing is being decided dilute the denominator. One "fraction of balls
  that cannot be reached" read 3.5% per tick and 19% per exchange.

Related: [[skill-meter-needs-escalation]].
