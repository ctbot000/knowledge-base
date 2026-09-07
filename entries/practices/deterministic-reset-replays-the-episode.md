---
title: A simulation that restores an identical state after each event replays the same episode, whatever the seed
tags: [simulation, testing, randomness]
added: 2026-09-07
---

## Fact

A reset that restores exact positions, phases and timers — a round restart, a
respawn, a kick-off — hands the simulation the same initial conditions every
time. If the generator is consulted only for occasional choices, the episode
that follows is bit-identical to the last one, and the seed makes no difference
to any of it.

The signature is unmistakable once you know it: **changing the seed changes
nothing**. Different seeds produce the same aggregate outcome, the same event
sequence, the same timings.

## Why it matters

That signature points at the generator, which is the wrong place. The natural
reading of "the seed does nothing" is that the RNG is not wired up — so the
investigation goes to the seeding, the plumbing, whether the state object even
holds the generator. All of it is fine. The repetition is coming from the reset,
which is upstream of the randomness and mentioned nowhere in the symptom.

It also silently destroys any statistics gathered over episodes: a hundred runs
of an identical episode look like a large sample and are one observation.

## How to apply

- Jitter what the reset restores, from the simulation's own generator: small
  offsets on positions, and a random phase on every periodic timer so agents do
  not decide in lockstep.
- Read "different seeds, identical outcome" as evidence about the **reset**, not
  about the generator — after confirming with one direct call that the generator
  does vary.
- Keep the jitter inside the seeded generator, so a given seed still replays
  exactly. Determinism across runs and variety across episodes are not in
  conflict; they are set by different things.
