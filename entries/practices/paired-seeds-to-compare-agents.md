---
title: Comparing two agent configurations needs paired seeds, or the noise floor swallows the effect
tags: [simulation, testing, benchmarking]
added: 2026-09-22
---

## Fact

In any scored game with a heavy tail, the per-game variance dwarfs the effect a
parameter change has. Measured on a card game whose scores run from 7 to 800:
per-game standard deviation was ~80 points, so even 5000 independent games give
a standard error of ~1.2 — while the settings under test differed by ~0.1.

Running the **same** configuration against itself is what reveals this. Four
blocks of 5000 games returned -0.47, +0.54, +0.74, -0.48 points per game. A
reading of -0.47 for an arm therefore means nothing; without the control block
it looks like a result.

Replaying every seed twice with the arms swapped between seats, and scoring the
half-difference, cancels the deal and the seat out of the comparison. On the
same workload the standard error fell from ~1.2 to ~0.03 — a 30x reduction for
2x the compute — and the ordering that was invisible before became clear at
z = -3.6 and z = -13.9.

## Why it matters

Unpaired self-play produces confident-looking numbers that are noise, so a
sweep "finds" an optimum that is a different value every time it is run. Tuning
then locks in a random choice, and the next sweep contradicts it, which reads
as the model being unstable rather than the measurement being underpowered.

The failure is silent: nothing errors, the sample size looks generous, and the
numbers are perfectly reproducible under a fixed seed — reproducibly wrong.

## How to apply

- Pair on the random input: same seed, arms swapped across seats, score
  `(a - b) / 2`. Common random numbers are the cheapest variance reduction
  available and need no change to the simulation.
- Always run an A-vs-A control arm. Its spread *is* your resolution; treat any
  arm inside it as unresolved rather than as a small effect.
- Report the standard error next to the mean. An arm difference below ~2 SE has
  not been measured, however many games were played.
- If several arms land inside the noise, pick on a secondary criterion you can
  actually defend, and say that is what you did.
