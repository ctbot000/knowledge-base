---
title: A clock topped up per unit of progress escalates on its own, and states its own survivability
tags: [game-design, balance, simulation]
added: 2026-09-11
---

## Fact

Giving a timed objective a flat allowance and shrinking it per level produces a
curve nobody can reason about: the allowance, the objective's length and the
rate at which work can be done all move independently, so difficulty spikes
wherever they happen to disagree and flattens again afterwards.

Draining the clock continuously and **topping it up by a fixed amount per unit
of progress** collapses all of that into one number. With a buffer of `M` units'
worth of time, a top-up worth `k` of a unit's cost, and an objective `L` units
long, the objective is survivable exactly while

```
actual seconds per unit / optimal seconds per unit  <  k + M / L
```

Send `k` from above 1 down through it and the shape follows for free: early on a
unit returns more than it cost, so clean work banks time; later it returns less,
so the clock net-drains however well it is played. No plateau to camp, and the
threshold is a closed form you can assert is monotone across every level the
game can reach.

## Why it matters

The threshold is the balance question stated directly — "how much slower than
optimal may a player be here?" — which a raw allowance in seconds never is. It
makes two otherwise awkward checks trivial: that difficulty never eases as it
climbs (compare consecutive thresholds), and that no level is impossible
(measure what strong play actually achieves, and compare the ratio against the
threshold at that level).

It also decouples the knobs. Tightening the supply rate or the objective's
length changes the unit cost, and the clock follows automatically instead of
silently becoming generous or unplayable.

## How to apply

- Model the unit cost rather than guessing the allowance, then set the buffer
  and top-up as multiples of it. The model only has to be proportional — the
  constants absorb the rest.
- Keep `M` fixed and move `k` alone, so a single monotone sequence drives the
  whole curve.
- Floor `k` just high enough that the threshold stays a little above 1.0; below
  that the objective is impossible for anyone.
- Assert the threshold's monotonicity in a test. It is a pure function of the
  level, so it costs nothing to check to level 60 and it catches a retune that
  reintroduces a spike.
- The player should see the top-up land. A clock that visibly jumps on each unit
  of progress teaches the rule without a word of explanation.

Related: [[skill-meter-needs-escalation]], [[multiplicative-bonus-separates-skill]],
[[measure-solution-density-before-tuning]].
