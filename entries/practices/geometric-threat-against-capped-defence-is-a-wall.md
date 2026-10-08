---
title: A threat that grows geometrically against a defence with a ceiling puts a wall at the level where they cross
tags: [game-design, balance, simulation]
added: 2026-10-08
---

## Fact

When the player's power is capped — a fixed number of build slots, a top
upgrade level, a maximum party size — and each level's threat is multiplied by
a constant, the curve has a wall, not a slope. Every level before the crossing
is a walkover (the defence is far ahead of a threat that starts small), every
level after it is impossible, and the crossing moves by a whole level for a
small change in the growth factor.

In one tower defense balance run, enemy health growing 1.38× per wave left the
first seven waves untouched by any strategy and made waves 8–10 unwinnable on
the smallest maps, where every slot was already maxed. 1.30× was trivial
throughout. Switching to a gentle polynomial (linear plus a small quadratic
term) and sizing it to the *smallest* map's fully built capacity gave a
graded curve.

## Why it matters

Every strategy fails at the same level, so it reads as a broken bot or a
broken level rather than a broken curve — and retries cannot help, because the
loser has already bought everything there is. Tuning the growth factor just
slides the wall.

## How to apply

- Compute or simulate the defence's capacity with everything bought, per map,
  and keep the last level's threat under the smallest map's ceiling.
- Prefer polynomial growth when power saturates; geometric growth only suits
  games whose power also compounds without limit.
- Measure tension per level (worst health reached, not just win/loss) across
  several strategies; a wall shows as unmarked levels followed by total loss.
- Give every map enough slots to reach that ceiling: slot count, not layout,
  set where the wall was in the run above.

Related: [[identical-skill-profiles-mean-a-blind-bot]], [[balance-knob-with-no-effect]],
[[difficulty-is-not-monotonic-in-one-resource]].
