---
title: A simulation's scheduled events must use its own accumulated clock, not wall-clock deadlines
tags: [testing, game-loop, simulation, frontend]
added: 2026-09-07
---

## Fact

A simulation that advances continuous state (`x += rate * dt`) usually also has
one-off events on timers — spawn something, roll for an event, fire a cooldown.
It is natural to store those deadlines as absolute timestamps:

```js
pet.nextSpawnAt = Date.now() + 90000;      // wall clock
if (now >= pet.nextSpawnAt) { spawn(); }
```

That puts the two halves of the simulation in different clock domains. The
continuous half lives in accumulated simulated time; the event half lives in
real time. They agree only while the simulation is stepped in lockstep with the
wall clock — which is exactly the case that stops holding as soon as anything
*drives* it: a test that advances the clock, a replay, an offline catch-up run
in coarse steps, a scrubbed timeline, a speed multiplier.

The continuous state then races ahead while the deadlines stay where the wall
clock left them, and no scheduled event ever fires.

## Why it matters

Nothing throws and nothing logs. The simulation visibly runs — stats move,
things age, rendering continues — so the missing half looks like a bug in the
event logic rather than a missing clock. Investigation goes to the spawn
condition, the probability, the guard clauses, all of which are correct.

It is worst in a test harness, because the harness is the thing that drives the
clock. A suite that advances a day of simulated time and asserts "no random
events occurred" passes for the wrong reason, and keeps passing.

## How to apply

- Keep one clock. Store deadlines in the simulation's own accumulated time —
  the same quantity the continuous state integrates:

  ```js
  pet.nextSpawnDay = pet.ageDays + 90 / SECONDS_PER_DAY;
  if (pet.ageDays >= pet.nextSpawnDay) { spawn(); }
  ```

- Wall-clock timestamps still belong at the boundary: one `lastTs` recording the
  last simulated moment, used to work out how much time to advance.
- The tell is a driven run where continuous state changes and discrete events
  never fire. Assert on both, not just on the numbers that move.

Related: [[driven-game-loop-needs-accumulator-reset]],
[[animation-lifetime-in-frames]].
