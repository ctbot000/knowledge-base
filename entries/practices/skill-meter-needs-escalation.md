---
title: A tug-of-war skill meter with no clock is always won by the patient player
tags: [game-design, simulation, balance]
added: 2026-09-05
---

## Fact

The common "keep the target inside the zone" minigame is a race between a gain
rate while on target and a loss rate while off it. With both rates constant and
no time limit, the outcome is decided entirely by the player's average on-target
fraction: above the break-even point they always win eventually, below it they
always lose. Skill sets the *length* of the attempt, not its result.

Because the break-even point is usually well under half, a mediocre player never
fails — they just take longer. Simulating a deliberately sloppy controller over
hundreds of attempts returns a 0% failure rate, which is the signature of this
shape rather than of generous tuning.

## Why it matters

The failure state is what makes the interaction a game; without it the meter is
a progress bar with extra steps, and no amount of adjusting the two rates
changes that, because both scale the same race. Adding a plain countdown fixes
the maths but replaces a skill test with a stopwatch, and it punishes the slow
start that makes a comeback feel earned.

## How to apply

- Escalate the loss rate rather than adding a clock: scale it by elapsed time
  and by progress, so a long attempt and a nearly-finished one both get harder.
  Multiplying the drain by roughly 2-3x over the first 15 seconds turns an
  endless stalemate into a decided one while leaving a clean run untouched.
- Keep a hard cap as a backstop so nothing can run forever, and give it its own
  failure message — it reads as a distinct outcome, not a bug.
- Let the failure meter recover more slowly than it fills, so repeated dips
  accumulate; resetting it on every recovery lets a player hover at zero.
- Validate with a bad controller, not a good one. A perfect simulated player
  says nothing; the useful signal is the failure rate of a deliberately laggy,
  noisy one across a few hundred attempts.
