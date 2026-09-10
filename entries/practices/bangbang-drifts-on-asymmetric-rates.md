---
title: A bang-bang controller with no deadband drifts toward the faster direction
tags: [control, simulation, testing, game-design]
added: 2026-09-11
---

## Fact

"Hold the value at `target`" written as `actuate = (value > target)` is a relay
with no hysteresis. At the switching point it chatters at the sample rate with
roughly a 50% duty cycle, so the value does not settle at `target` — it moves at
the *average* of the two rates.

That average is only zero if the two directions are symmetric. Where they are
not — a hook that rises at 1.35× the speed it sinks, a thruster stronger than
gravity, a fill rate above the drain rate — the value walks steadily toward the
faster direction and leaves the band entirely.

## Why it matters

The controller reads as obviously correct, and it is correct in intent, so the
drift gets attributed to the plant: to buoyancy, to a clamp, to an integration
error. In a test harness it silently invalidates the scenario, because the run
that was supposed to hold a depth spends its time somewhere else and reports
whatever lives there instead.

## How to apply

- Give it a deadband: `if (v > hi) up = true; if (v < lo) up = false;` with the
  band wider than one step of the faster rate. That is the whole fix.
- Size the band from the rates, not by eye: `lo`/`hi` at least
  `maxRate × dt × 2` apart.
- Suspect this whenever a hold-at-a-value loop ends up pinned at one extreme.
  Symmetric rates hide it completely, so it appears only once the two directions
  are tuned differently.
