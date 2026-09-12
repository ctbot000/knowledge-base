---
title: A spacing rule enforced only at spawn time does not hold once the entities move
tags: [procedural-generation, game-design, simulation]
added: 2026-09-12
---

## Fact

Constraints checked when an entity is placed — minimum gap, no more than N in a
window, never block every lane — describe the moment of placement and nothing
after it. Entities that steer, drift or travel at different speeds reassemble
into exactly the configuration the rule forbade, somewhere downstream of it.

The check has to run again while the entity is still free to act. Where there is
also a commitment deadline (a point past which moving is unfair to the player),
that deadline is the last place the rule can be enforced.

## Why it matters

The rule is present, is correct, and is the first thing read when the forbidden
configuration is reported — so the placement code looks exonerated and the
search moves to the movement code, which is also correct. Neither is wrong; the
constraint simply has no authority over the interval between them.

It is also invisible at low densities, where the configuration is rare enough to
look like bad luck, and arrives as the density knob is raised.

## How to apply

- Re-evaluate the constraint at every point the entity may still act, not only
  at creation, and treat a violation as overriding whatever cooldown or
  randomness normally gates a decision.
- Look for a resolution that does not need a free slot. In a lane-blocking case,
  pulling one entity into a lane another already occupies frees a whole lane —
  two nose-to-tail is a gap where three abreast is a wall.
- Assert the outcome, not the rule. Measure how often the forbidden
  configuration occurs over a long automated run; a structural guarantee that
  cannot be maintained end to end is better stated as a rate.
