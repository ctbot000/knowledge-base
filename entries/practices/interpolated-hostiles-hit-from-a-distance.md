---
title: A hostile drawn with snapshot interpolation hits the locally predicted player from a step away
tags: [game-design, networking, game-loop]
added: 2026-10-11
---

## Fact

Remote entities are usually drawn a fixed delay in the past, interpolated
between authoritative snapshots, while your own avatar is predicted locally and
drawn *now*. Contact is decided by the authority on current positions. So at
the moment a chasing enemy touches you, it is drawn `speed × (interp delay +
snapshot age)` behind where it is: at 3.4 m/s, a 260 ms delay and 200 ms
snapshots, it is still 0.85 m off when the knockback hits — with no network
latency at all. The same delay shows the enemy's own reaction to your hit
(knockback, recoil) a snapshot interval or more after the impact cue.

## Why it matters

Combat reads as unfair or "floaty" — hit from a distance, hits that land on
nothing — and it looks like a hitbox or tuning problem. Shrinking hitboxes or
raising snapshot rates only nibbles at it; the cause is mixing two time bases
in one interaction.

## How to apply

- Draw entities that interact with the local player on the local player's
  time base: extrapolate from the last snapshot's velocity, capped to about a
  snapshot interval, and zero the velocity in states where the entity stands
  still. Keep plain interpolation for ambient entities.
- On each new snapshot, store the gap between where it was drawn and the new
  guess as an offset that decays over ~100–150 ms, instead of jumping.
- Extrapolate horizontally only for hopping/jumping bodies; vertical arcs are
  too short to guess and overshoot into the ground.
- On a hit event, start the expected reaction locally at once (knockback away
  from the attacker) until the next snapshot takes over.
- Measure it: log the drawn gap when the contact event arrives; it should be
  about zero.
