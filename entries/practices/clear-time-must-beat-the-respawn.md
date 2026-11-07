---
title: An objective that needs an area empty is impossible once clearing it outlasts the respawn
tags: [game-design, balance, simulation]
added: 2026-11-07
---

## Fact

Where enemies come back a fixed time after they die, and the goal needs none of
them present, the area can only ever be emptied if the last one falls before the
first one returns: total enemy health divided by the player's damage rate has to
stay under the respawn time.

That is a cliff, not a slope. Adding one tough enemy to a group makes the fight
harder only until the sum crosses the respawn time; past it the first enemy is
back before the last is down, and no amount of play clears the area. Damage taken
matters too: a player who has to retreat to recover gives back the whole window.

## Why it matters

Each enemy looks fair on its own, and a strong player with a strong weapon clears
the group, so playtests pass. The player it blocks is the weaker one on a required
step, who sees an endless fight rather than a wall, and it reads as "hard".

## How to apply

- Compute the sum for the weakest loadout expected at that point:
  `sum(health) / damage_per_second < respawn_seconds`, with room to spare.
- Give the strongest enemies a role that does not respawn: one that stays dead
  until the area resets costs its health once rather than every cycle.
- Scale those to the stage and the number of players rather than fixing their
  health, so the same enemy suits both an early solo player and a late group.
- A simulated fight with the weakest weapon is cheap, and answers it directly.
