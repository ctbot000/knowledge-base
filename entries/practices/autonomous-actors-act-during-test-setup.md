---
title: An entity that acts on its own schedule also acts while a test is staging the scene
tags: [testing, simulation, game-design]
added: 2026-09-12
---

## Fact

Simulation tests are usually written as: build the world, place the entities,
trigger one action, assert on the result. But any entity that decides for
itself when to act — a turret with a cooldown that starts at zero, a spawner,
an AI on a timer — starts acting on the first step, which includes the steps
the test runs to let the scene settle.

So by the time the action under test is triggered, the entity has already
acted once or twice on its own, and the assertion counts all of them.

## Why it matters

The failure is asymmetric, and that is what makes it dangerous. A test
asserting "this action affects **exactly one** target" fails, and looks like a
bug in the code under test. A sibling test asserting "this action affects **at
least three**" passes — on the extra actions, not on the one it meant to
measure. So the pair reads as "one real bug, one healthy test" when in fact
neither test is measuring what it claims, and the passing one will keep passing
after the behaviour it covers is broken.

It also hides behind a plausible first hypothesis: the obvious suspect is the
action's own radius or target selection, which is fine.

## How to apply

- Disable autonomy before staging, not after: set the cooldown to something
  huge *before* the settling steps, trigger the one action, then set it huge
  again, because triggering it normally resets the timer.
- Prefer asserting an exact count over a lower bound wherever the mechanic
  allows one. `>= 3` cannot tell three from six, and that is the slack the
  extra actions hide in.
- When a scene needs entities held still, zero the rate they move by rather
  than writing their derived position: positions recomputed from a canonical
  parameter each step will snap back and silently relocate the whole scene.

Related: [[flawless-player-measures-survival]], [[puzzle-tests-must-parse-the-clue]].
