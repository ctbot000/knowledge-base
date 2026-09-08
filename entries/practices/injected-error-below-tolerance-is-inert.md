---
title: Injected aim error does nothing until it exceeds the catcher's own tolerance
tags: [game-design, balance, simulation]
added: 2026-09-08
---

## Fact

Giving an AI opponent an aim error so that it sometimes misses only works once
the error can clear the tolerance the catcher already has. A paddle that
intercepts anywhere along its length forgives any error smaller than half that
length plus the projectile's radius; inside that window the opponent performs
exactly like a perfect one.

An error dial whose whole range sits under the threshold is therefore inert. It
reads as tuned — the number exists, it is sampled, it visibly moves the aim point
— and the miss rate stays at zero.

## Why it matters

An opponent that cannot miss makes exchanges unbounded, and the symptom surfaces
somewhere else entirely: rounds that never end, a test that runs to its iteration
cap, a difficulty ladder whose tiers all behave identically.

Raising the dial by ordinary increments then changes nothing at all until it
crosses the threshold, where the miss rate climbs steeply. So the two natural
readings are both wrong: that the knob is broken, and — after one increment too
many — that the opponent is now hopeless.

## How to apply

- Write the threshold down in the same units as the error and compare them
  directly: for a paddle, half the catching surface plus the projectile radius.
- Tune toward a miss probability rather than an error magnitude. For an error
  drawn uniformly from ±e against a threshold t, that probability is `(e - t)/e`,
  so a 20-30% miss rate needs e at roughly 1.3-1.4x t.
- Scale the error with the pressure of the moment — projectile speed, exchange
  length — instead of adding a timer. Long exchanges then end on their own.
- Confirm the dial moves the outcome at all before tuning it further.

Related: [[balance-knob-with-no-effect]], [[simulated-error-is-per-decision]].
