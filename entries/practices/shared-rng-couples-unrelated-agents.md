---
title: Agents that draw from one shared random stream change each other's behaviour when one is added
tags: [simulation, testing, randomness]
added: 2026-10-04
---

## Fact

When every entity in a seeded simulation takes its random numbers from one
generator, in list order, adding an entity — or a whole new kind — shifts
every draw after its own. Every other entity then follows a different
trajectory, although nothing about it changed.

## Why it matters

Seeded tests of the existing behaviour move or fail the moment the new kind
arrives, and the new feature gets blamed for an interaction that does not
exist. It also exposes how much those tests leaned on one lucky seed: a
"penguins sleep ashore at night" share read 0.75 on the tested seed and
anything from 0.13 to 1.0 on ten others, before anything was added.

## How to apply

- Give each independent subsystem its own stream, seeded from the world seed
  plus a constant of its own, and use it for everything it draws, including
  what it draws when its entities are created.
- Assert the separation: run the same seed with and without the new entities
  and require the old entities' traces to be identical.
- When a seeded statistic moves after a change, rerun the same seeds with the
  change switched off before looking for a behavioural cause, and widen the
  test to several seeds if the spread across seeds is large.
- Related: [[paired-seeds-to-compare-agents]], [[deterministic-reset-replays-the-episode]].
