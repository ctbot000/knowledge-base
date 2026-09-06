---
title: A fixed-timestep accumulator and its timestamp baseline are one piece of state
tags: [testing, game-loop, requestAnimationFrame, frontend]
added: 2026-09-06
---

## Fact

The standard fixed-timestep loop keeps two related values — the last frame
timestamp and the leftover-time accumulator:

```js
if (!last) last = now;          // resets the baseline, but not `acc`
let dt = (now - last) / 1000;
last = now;
acc += dt;
while (acc >= FIXED_DT) { update(FIXED_DT); acc -= FIXED_DT; }
```

Resetting one without the other breaks the loop, and a timestamp that moves
backwards breaks it hard: `dt` goes negative, `acc` goes deeply negative, and
the `while` never runs again until real time repays the gap. Nothing throws.
Rendering continues, input is still accepted, and the simulation is simply
stopped.

Animation-frame timestamps are monotonic within one document, so this surfaces
wherever the loop is driven rather than scheduled: tests feeding chosen
timestamps, replays, a restarted loop, a timeline scrubbed by hand.

## Why it matters

It is worst in the harness that is supposed to prove the loop correct. A
frame-rate independence test that restarts each run from a lower timestamp
reports zero simulated distance at the higher rates — which reads as "the game
breaks above 60Hz", a plausible and completely wrong conclusion, and one that
sends you into the physics rather than into the harness.

The silence is the trap: a stopped accumulator looks exactly like a game that
runs, because everything except `update` still runs.

## How to apply

- Reset the pair together: `if (!last) { last = now; acc = 0; }`.
- Clamp the delta at both ends, not just the top:
  `dt = Math.min(dt, MAX_FRAME_DT); if (dt < 0) dt = 0;`
- Have each driven run start from a timestamp above the previous run's last one,
  or reset the baseline explicitly between runs.
- Assert frame-rate independence on the app's own accumulated time, not on
  wall-clock: the same wall interval at 30/60/120/144Hz must produce identical
  state. A zero at one rate is the signature of this bug, not of the physics.

Related: [[animation-lifetime-in-frames]], [[hidden-surface-delivers-no-frames]].
