---
title: A telegraphed attack aimed at where the player stands is dodged by walking in a circle, whatever its speed
tags: [game-design, combat, ai, simulation]
added: 2026-11-25
---

## Fact

An attack that shows its target first lands a wind-up plus a travel time later. A
player who keeps walking has covered several body widths by then, so every lane,
projectile and landing spot aimed at the position at wind-up misses. No faster
projectile fixes it, because the wind-up alone is enough. Aiming only at the
predicted position is beaten the same way, by stopping.

## Why it matters

The fight has readable attacks and still contains no decision: holding one
direction is safe, so players circle, never learn the dodge or the parry, and call
it easy or boring. Damage and speed tuning do not touch it. A bot that strafes
round its target shows it at once: a boss fight measured over minutes with no
damage taken and no counter-attack triggered.

## How to apply

- Choose each attack's target at random between the current position, part of the
  way, and the full predicted one (about a third each), from the target's smoothed
  velocity times the time until the attack lands. Neither circling nor standing
  still is then safe, and reading the marker is.
- Cap the lead (a few body lengths) and ignore the velocity of dashes, knockback
  and teleports, which say nothing about where the player is going.
- Give thrown things a slow turn rate instead where they are meant to be hit back:
  they must arrive to be answered.
- Scale how much of the lead is used by level; it is a difficulty knob that needs no
  extra damage.
