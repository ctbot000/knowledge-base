---
title: A balance change that does not move the outcome means the dominant term is elsewhere
tags: [game-design, balance, simulation]
added: 2026-09-07
---

## Fact

When a tuning parameter is changed and the measured outcome does not move, that
is a fact about the model, not about the parameter.

Halving a boss's projectile damage in a scripted fight left the win rate, the
time of death and the boss's remaining health identical across every seed. The
reason was that projectiles were never the problem: most of the health loss was
self-inflicted blast damage from the player's own bombs. Logging each health
change with what caused it found it in a single run.

The same signature shows up whenever one term dominates a sum — contact damage
swamping ranged damage, one enemy type swamping the rest, a fixed cost swamping
a scaling one.

## Why it matters

The natural reading of "that change did nothing" is "the change was too small",
so the parameter gets pushed further and further from a sensible value while the
term that actually decides the outcome is never touched. The design ends up
mis-scaled in two places at once, and every later conclusion drawn from the same
harness inherits the blind spot while the numbers keep agreeing with each other.

## How to apply

- Attribute before tuning. Log every change to the resource being balanced
  alongside its cause, then total by cause. The dominant term is usually a
  surprise.
- Treat an inert knob as a stop signal, not as an invitation to a bigger change.
- Include self-inflicted and environmental sources in the attribution. They are
  the ones nobody thinks to model, and the ones a scripted agent walks into.
- Check that the attributed totals sum to the observed change; a shortfall is a
  source you have not accounted for.

Related: [[simulated-error-is-per-decision]].
