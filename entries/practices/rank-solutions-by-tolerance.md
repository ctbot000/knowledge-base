---
title: In a chained-reflection aiming problem, most solutions are knife-edge, so rank candidates by tolerance rather than by success
tags: [game-design, search, simulation]
added: 2026-09-08
---

## Fact

Where a shot has to survive several reflections before it counts — a bank shot,
a ricochet puzzle, a trick-shot validator — a brute-force search returns mostly
solutions that work only at one exact aim. Each bounce multiplies the angular
error, so the set of successful inputs is a dense scatter of near-zero-width
slivers with a few genuinely wide bands hidden among them.

Measured over a three-cushion billiards search, the *first* scoring shot found
from a random position tolerated a median of **0.04°** of aiming error. Re-ranking
the same candidates by how many nearby shots also score lifted the median chosen
window to **0.58°**, with the best above 1.5°.

A success/fail verdict cannot tell the two apart: both are "it scores".

## Why it matters

An agent aiming at 0.04° windows misses almost everything, which reads as broken
execution, bad physics, or a model too chaotic to play. The tempting fix is to
shrink the agent's error until it hits, producing an inhumanly precise actor that
is still fragile; a human handed the same solution cannot execute it at all.

It also inverts a difficulty design. With tolerance ranking added and the
execution error left untouched, a strong opponent went from making 12% of its
shots to 68%. Search depth barely moved the number.

## How to apply

- Score a candidate by re-simulating it under small perturbations of every input
  a real actor cannot control exactly — aim, power, timing — and keep the
  fraction that still succeed. Ten probes is enough to separate the tiers.
- Rank by that fraction, not by the raw verdict, and take the widest.
- Keep the search cheap and spend the budget here; sampling more knife-edge
  solutions does not help.
- The same measurement sizes the difficulty knob: an error distribution narrower
  than the chosen window succeeds, one wider than it fails, and the ratio is
  what the player feels.
