---
title: A placement bot scored on total coverage stacks every unit on one spot and measures itself
tags: [game-design, testing, simulation]
added: 2026-09-12
---

## Fact

A scripted player used to measure a level's difficulty needs a rule for where
to put things. The obvious one — score each candidate position by how much of
the threat it covers, take the best — is degenerate: the scoring does not
change as units are placed, so every unit is sent to the same maximum, and the
bot ends up with its whole force piled on one cell.

Scoring **marginal** coverage fixes it. Weight each point of the threat by how
well it is already covered, so a candidate is worth what it adds:

```
score(cell) = Σ over threat points within range of (weight / (1 + already_covering))
```

## Why it matters

The measurement is then reported as a property of the level. A concentrated
bot covers a fraction of the map, so everything downstream reads as too hard,
and the fix gets applied to the level's numbers instead of to the bot. In one
measured case the same level went from 43% to 99% coverage on this change
alone — with no change to the level at all.

The tell is a bot whose coverage barely improves as it is given more resources,
or skill tiers that all die at the same point: if every tier of player fails
identically, the variable being measured is not the player.

## How to apply

- Score marginal contribution, never total, for any greedy placement policy.
- Report the bot's coverage of each threat alongside its win rate. Coverage
  near zero for one threat is a level or bot fault, not a difficulty reading.
- Add a small random jitter to the score so ties do not all resolve the same
  way, and use its magnitude as the bot's skill dial.
- Sanity-check that skill tiers actually separate before trusting any number
  the harness produces.

Related: [[identical-skill-profiles-mean-a-blind-bot]], [[bot-camping-on-target-inflates-difficulty]].
