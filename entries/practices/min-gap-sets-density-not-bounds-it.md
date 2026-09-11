---
title: A minimum-spacing rule sets the output density rather than bounding it
tags: [procedural-generation, game-design, algorithms]
added: 2026-09-11
---

## Fact

Place items greedily from a candidate stream, rejecting any that falls within
`gap` of one already placed, and the result converges on `1/gap` items per unit
wherever candidates are dense. The constraint does not limit density to
something below the source's — it *replaces* the source's density with its own.

So a spacing rule tuned to "the closest two items a player can handle" produces
that worst case continuously, everywhere the candidates allow it, instead of
only at the peaks the source actually had.

## Why it matters

The tuning knob reads backwards. Widening the gap to make the output easier also
strips the sparse passages, because the same rule is the only thing deciding
both; narrowing it to keep detail saturates everything. Nothing in the output
carries the shape of the input any more, which is usually the reason the input
was chosen as the source.

It hides whenever the candidate stream is sparse — a melody with rests looks
fine — and appears the moment a continuous source is added to fill the gaps,
which is exactly the change intended to make the output *more* even.

## How to apply

- Separate the two constraints. Keep the pairwise gap for what the hands or eyes
  can physically separate, and add a rolling-window cap — count what is already
  placed in [t-w, t+w] and reject past a budget — for how much is sustainable.
- Place candidates in priority order, whole source first, so the density budget
  is spent on the signal and only the remainder goes to filler.
- Measure the result as a distribution, not a total: peak per window and longest
  empty run say what a mean rate cannot.
