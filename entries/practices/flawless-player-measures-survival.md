---
title: A flawless simulated player measures an opponent's survival, never its win rate
tags: [game-design, testing, simulation]
added: 2026-09-08
---

## Fact

A controller that plays perfectly never concedes, so every match it plays ends in
a shutout whatever it is playing against. An assertion of the form "the hard
opponent should take some points" is unsatisfiable by construction, and a sweep
across difficulty tiers returns the identical scoreline for all of them.

What a flawless player does measure is how long the opponent lasts: rally length,
time to concede, returns made before the miss. That separates tiers cleanly while
the score cannot.

Win rates need a *fallible* controller, one carrying an explicit error term. The
two answer different questions — the flawless run proves a tier is reachable and
beatable at all, the fallible run proves the tiers are different walls rather
than the same one.

## Why it matters

The degenerate scoreline looks like a balance bug. Identical shutouts across
easy, normal and hard read as "difficulty does nothing", which sends the
investigation into the opponent's tuning, where there may be nothing wrong at
all. The test was measuring a quantity that cannot vary.

Writing the wrong assertion first is the easy mistake, because "the hard opponent
should score sometimes" is exactly how the requirement is stated in prose.

## How to apply

- Against a flawless player, assert on survival: mean rally length rising per
  tier, plus a lower bound on the ratio between the easiest and the hardest.
- Assert separately that the flawless player wins every tier. That is the
  reachability check, and it is all the scoreline is good for.
- Keep a second controller with an explicit error term for win-rate assertions,
  and drive it from a seeded generator so a failure replays exactly.
- Sweep several seeds and compare means. Rally length against a near-perfect
  opponent is wildly distributed — single runs differ by an order of magnitude —
  so one sample proves nothing.

Related: [[tracking-target-vs-slew-rate]], [[simulated-error-is-per-decision]].
