---
title: A failure state that cannot be forced means some income is uncorrelated with the thing that fails
tags: [game-design, balance, simulation]
added: 2026-09-19
---

## Fact

A test that deliberately drives a system into collapse — strip the revenue,
keep the payroll, run the clock — and finds it *recovering* has not found a
resilient system. It has found an input that is keyed to the wrong signal.

The usual shape is a windfall gated on a lagging indicator. Donations rolled
for on reputation, a grant sized by last quarter's rating, a retry budget
refilled on a smoothed average: the trigger keeps firing long after the
activity it is supposed to reward has stopped, because the indicator it reads
decays far more slowly than the activity did.

A small, regular windfall then floats the system just above its floor for ever.

## Why it matters

The failure mode is invisible from the healthy side. In normal operation the
windfall is a rounding error against real revenue, so no balance pass notices
it, and no player or operator ever reports it.

It only surfaces as an absence: the bankruptcy path, the circuit breaker, the
degraded mode — written, reachable in principle, and never once entered. That
is indistinguishable from "we are doing well", so it is not looked for.

## How to apply

- Gate every rescue on the **live** driver, not the lagging one: footfall for
  the day rather than accumulated reputation, requests actually served rather
  than a rolling success rate.
- Write the adversarial test. Set up the collapse on purpose and assert the
  system reaches the failure state; a passing "it survived" is the bug.
- Size the windfall against the burn it must not cover, not against the
  revenue it is meant to supplement.

Related: [[extraction-economy-must-pay-at-tier-zero]],
[[zeroed-recovery-is-a-trap-not-a-cost]].
