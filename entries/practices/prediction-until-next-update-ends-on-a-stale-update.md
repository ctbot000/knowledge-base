---
title: A client prediction that lasts "until the next server update" is cancelled by an update sent before the server acted
tags: [networking, game-design, prediction]
added: 2026-11-07
---

## Fact

Drawing an effect at once and dropping the prediction as soon as a new state
update arrives assumes that update already includes the effect. Updates are sent
on their own timer, so the next one was often built before the action was
processed, or carries only its first few milliseconds. It cancels the prediction
and the object snaps back to following a state that has hardly changed; the real
motion shows up a tick later.

The longer the delay before the predicted motion starts (a hit-stop, a wind-up),
the surer it is: with updates every 150-200 ms and a stop of 70-170 ms, one lands
inside the stop nearly every time.

## Why it matters

A knocked-back monster hops on the spot, then slides away 150 ms late, on some hits
and not others. It reads as a sluggish, inconsistent hit, varies with tick phase,
and usually looks fine in a test that happens to miss the tick.

## How to apply

- Hold the prediction for a fixed time, and take the further of the two along its
  direction: `max(progress in the latest update, predicted curve)`. Updates that
  have caught up win, stale ones change nothing.
- Ending the hold is a discontinuity like any correction: fade the difference out
  from where the object was last drawn.
- Reproduce it on a stepped clock, or the tick phase hides it: log the object's
  position per frame across a few hits and look for the stall.
