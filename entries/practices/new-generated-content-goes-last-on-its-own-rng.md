---
title: New procedural content keeps every existing seed's output only if it is generated last, from a random stream of its own
tags: [procedural-generation, randomness, testing, simulation]
added: 2026-10-04
---

## Fact

A generator that draws everything from one seeded stream produces a different
world for every seed the moment a new step consumes a draw, or merely changes
whether an earlier step accepts a candidate (a new "keep clear of X" check in a
rejection loop). Everything drawn after that point shifts. Adding the new
feature at the end of generation, from its own stream (`new Rng(seed ^ CONST)`),
and making it edit the finished result (clearing what is in its way) leaves
every earlier step bit-for-bit identical.

## Why it matters

Tests pinned to seeds silently become tests of different content. Statistical
assertions that only ever passed on a lucky seed ("most agents do X on seed N")
start failing, and the failure points at code the change never touched.
Agent simulations sharing one stream make it worse: a single entity nudged at
t=0 reorders every later draw, so the whole run diverges even when the new
content is far from anything being measured.

## How to apply

- Put the new step after all existing ones; give it its own derived seed. Do
  not add constraints to earlier steps' accept/reject loops; let the new step
  remove or move what conflicts instead.
- Verify by diffing old and new output with the new step switched off: they
  must match exactly.
- When a seed-pinned behavioural test still fails, measure the property across
  many seeds on the old code before blaming the change: if the old code already
  fails on a large share of them, the test is seed-lucky, and that is a
  separate bug.
