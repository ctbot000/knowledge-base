---
title: A state that zeroes a recovery rate is a dead end, not a penalty
tags: [game-design, balance, simulation]
added: 2026-09-12
---

## Fact

Two resources, where running the first one out sets the second one's regeneration
to zero, is not a hard difficulty setting. It is an absorbing state: the only
way to restore the first resource is to reach somewhere, reaching anywhere costs
the second, and the second no longer comes back.

Nothing reports it, because the player is not dead. They are alive, static, and
holding a bar that will never move again. In a simulated run it shows up as a
long tail of episodes that neither win nor lose, sitting at the timeout.

A multiplier does the intended job without the trap. Cutting recovery to a third
makes the state painful and slow while leaving a route out of it, and the shape
of the difficulty curve is almost identical up to the moment the old version
became unrecoverable.

## Why it matters

The check that would catch it — win rate — reports the same number whether the
run was lost or stalled, so the design reads as "too hard" and gets tuned by
softening the drain, which does not remove the absorbing state, only postpones
it.

The same shape appears outside games: a rate limiter whose backoff is fed by the
thing it is throttling, a cache whose refill needs the capacity it ran out of, a
retry budget consumed by the retries that would earn it back.

## How to apply

- Never multiply a recovery rate by zero. Floor it, even at 10 percent.
- Give the depleted resource at least one source that is free: a region where it
  refills on its own, or an action that costs nothing else.
- Instrument for stalls, not just losses. Count episodes that end in neither
  outcome — that bucket is where absorbing states hide.
