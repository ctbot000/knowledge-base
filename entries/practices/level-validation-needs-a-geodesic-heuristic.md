---
title: A level solver guided by straight-line distance reports maze levels as impossible
tags: [game-design, level-design, testing, algorithms]
added: 2026-09-07
---

## Fact

Validating that an authored level is *completable* means searching over the
actions a player actually has — a shot angle and power, a jump, a move — and
that search needs a heuristic to rank the states it reaches. Euclidean distance
to the goal is the obvious choice and it is wrong as soon as walls exist.

Inside a spiral, a ring corridor or any doubling-back layout, the goal is
already near in a straight line and gets no nearer by making progress, so a
search ordered on that distance never leaves the outer arm. It returns "no
solution found" for a level that is perfectly playable.

A breadth-first distance field from the goal over the open cells — distance
*around* the obstacles — orders the same states correctly, and costs one grid
flood fill per level.

## Why it matters

The false negative lands on exactly the levels worth validating: the intricate
ones. A straight corridor passes either way, so the check looks like it works
right up to the point where it starts lying, and the lie says the level is
broken rather than the validator. Time then goes into redesigning a good level.

The reverse error is quieter still. Reachability — can a point-sized thing walk
from start to goal — is a different question from completability, and it passes
on levels the player's real move set cannot finish. A validator wants both.

## How to apply

- Flood-fill a distance field from the goal once per level, then rank search
  states by the field, never by `hypot(dx, dy)`.
- Inflate obstacles by the agent's radius when building the field, minus a
  cell's slack: a fill walking cell centres at full radius closes corridors the
  agent can really take.
- Run both checks and report them separately — a flood fill for reachability, a
  beam or breadth-first search over real actions for completability.
- Give the search a stroke/move budget tied to the level's own difficulty rating
  (par, a target time), so the check tightens as the design intends.

Related: [[no-guess-puzzle-generation]].
