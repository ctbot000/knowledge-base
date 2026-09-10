---
title: A test harness that steps only the simulation is a different system from the one the frame loop runs
tags: [testing, game-loop, graphics, automation]
added: 2026-09-11
---

## Fact

Driving a real-time app from a script usually means calling its `update(dt)` in a
loop and rendering once at the end, because rendering is the expensive part. That
is only equivalent if nothing integrates inside the render path — and in practice
plenty does: camera smoothing, interpolated transforms, LOD selection, anything
written as `current += (target - current) * rate`.

Batch 200 updates behind one render and such a value advances one step, not 200.
The simulation is correct, the picture is of a state the app would never show,
and the two disagree by exactly the amount that was skipped.

## Why it matters

It presents as a bug in whatever lives in the render path. A camera that has
integrated once looks like a camera that will not converge — so the search goes
into the follow code, the lerp rate and the target computation, all of which are
fine. Screenshots taken from the harness then keep confirming it.

The same shape catches anything else the frame does outside `update`: input
sampling, overlay sync, visibility toggles driven per frame.

## How to apply

- Have the harness call the app's own frame function, the whole one, N times.
  If rendering is too slow for that, factor the frame into `advance(dt)` (sim +
  every per-frame integrator) and `draw()`, and drive `advance` N times.
- The giveaway is a value that converges in the running app and stalls under the
  harness. Compare it after `n` harness steps against `n` real frames before
  blaming the value's own code.
- The timestamp half of this is [[driven-game-loop-needs-accumulator-reset]].
