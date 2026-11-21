---
title: Knockback whose return trip outlasts the attack cooldown lets a player win a melee fight without moving
tags: [game-design, combat, ai, simulation]
added: 2026-11-21
---

## Fact

If a hit knocks an enemy out of reach and its AI then chases straight back, it
re-enters reach a fixed time later. When that return trip takes at least as long
as the attacker's cooldown, the enemy arrives just as the next swing is ready:
standing still and attacking each time it comes back wins every duel without
being touched, and extra enemy health only lengthens the same metronome. An
enemy too heavy to be knocked out of reach falls into the opposite degenerate
case: stand and trade, attacking at the maximum rate and taking contact damage
on a fixed beat.

## Why it matters

Every hit lands with full feedback, so clips and playtests look fine, and the
fights get called "boring" rather than broken. More hit-stop, flashes or screen
shake cannot help: the fight contains no decision. A contact-damage enemy with
no wind-up gives the player nothing to read or dodge either, so movement only
matters for running away.

## How to apply

- Simulate a player that never moves and attacks the instant an enemy is in
  reach, with the real cooldown and wind-up, against every enemy type on the
  authoritative code. Zero damage taken means that enemy is not a fight. A low
  share of the fight spent in reach (about a third) is the stun-lock's other
  signature; the rest is waiting.
- Give enemies an attack that starts outside the player's reach: a visible
  wind-up, a lunge faster than the player walks, then a recovery window that is
  the safe time to hit. Standing still must lose to it; a step aside must beat it.
- Do not let the return path be a straight line into the swing: circle, hold
  back, or come in on an attack of their own instead of walking into the fist.
- Re-run the same bot after each change; it measures the change directly.
