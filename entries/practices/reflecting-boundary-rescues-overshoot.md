---
title: A reflecting boundary turns a projectile game's overshoot into a second attempt at the target
tags: [game-design, collision, balance]
added: 2026-09-07
---

## Fact

In a game where a projectile must pass through a target, any wall the projectile
can bounce off and still reach the target removes the penalty for too much
power. A ceiling above the target is the usual culprit: the over-powered lob
rises, rebounds, and drops back through on the way down.

The tell is in the shape of the scoring window, not in any single shot. Sweeping
the whole (angle, power) input space, the window's upper bound sits exactly at
the input cap for *every* launch position — full power always scores. Removing
the boundary collision bounds the window on both sides, and the same sweep then
shows distinct per-position windows.

## Why it matters

It collapses the skill gradient without breaking anything. Calibrating power is
the core act of the game, and a rebound surface makes the dominant strategy
"maximum power, steep angle" from everywhere — which needs no calibration at
all. Playtesting one shot at a time will not surface it, because each individual
rebound looks like a lucky bounce rather than a reliable strategy.

The boundary is usually added for an unrelated reason — keeping the projectile
on screen, or "so it can't escape the level" — so nothing about the change
announces itself as a balance decision.

## How to apply

- Sweep the full input space and assert the scoring window is bounded on both
  sides. A window whose upper edge equals the input cap is this bug.
- Prefer letting the projectile leave the play area over reflecting it, and
  track it with an edge indicator so the player still knows where it is.
- Where a boundary must exist, make it absorbing or heavily damped, so no
  rebound retains enough energy to reach the target.
