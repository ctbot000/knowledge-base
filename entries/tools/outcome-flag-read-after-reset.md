---
title: An outcome flag read after the round resets reports the reset value, not the outcome
tags: [testing, instrumentation, game-loop]
added: 2026-09-07
---

## Fact

Instrumentation that classifies an attempt by reading state *after* the attempt
finishes gets whatever the reset wrote, because completing an attempt and
preparing the next one are the same transition.

Classifying shots by reading "did it touch the rim" once the loop had ended
reported zero contacts on every scoring shot — a clean 100% rate. The flag was
real and correct; it had simply been cleared microseconds earlier by the routine
that placed the next ball.

## Why it matters

The wrong number lands in the plausible range and flatters the thing being
measured, so it reads as a result rather than as a bug. Nothing throws, and the
probe looks like it is measuring the right quantity.

The only signal is a second measurement of the same thing taken at the correct
moment: a counter the system incremented at the scoring event said the opposite
(zero clean shots in twenty-one). Two disagreeing measurements of one quantity
is the tell, and the later-sampled one is the one to distrust.

## How to apply

- Sample classifying state at the instant the outcome fires — poll for the event
  inside the stepping loop and read the flags there — not after the loop exits.
- Prefer a counter the system maintains itself at the event over reconstructing
  the classification from outside; the internal one cannot be sampled late.
- When two measurements of the same quantity disagree, check when each was taken
  before checking what each computed.
