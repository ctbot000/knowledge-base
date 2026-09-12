---
title: A timeline read from an absolute clock absorbs a jump by moving its epoch, not by clamping a delta
tags: [game-loop, timing, frontend]
added: 2026-09-12
---

## Fact

An accumulating loop adds `dt` per frame, so a bad frame is handled by clamping
that `dt`. A timeline whose position is `clock() - epoch` has no delta to clamp
— the jump is already inside the answer. The only place to absorb it is the
epoch:

```js
const t = clock() - epoch;
const step = t - prev;
if (step > MAX_STEP || step < 0) {
  epoch += step - Math.max(0, Math.min(step, MAX_STEP));
}
```

Jumps are ordinary, not exotic: an audio context suspending and resuming, an
output device changing, an occluded or throttled tab, a machine waking.

## Why it matters

Applying the jump makes the timeline skip, and everything scheduled inside the
skipped span is processed in a single frame — expiring, resolving or failing
together. That reads as a logic bug in whatever consumed them, because the
failure is a burst rather than a drift, and the clock looks healthy both before
and after.

## How to apply

- Decide per system whether a gap should be skipped or absorbed. Absorb it
  wherever a person is reacting to the timeline; skip it wherever the timeline
  models real elapsed time, such as an idle-progress economy.
- Absorb by moving the epoch, and clear `prev` at every legitimate discontinuity
  — a start, a seek, a resume — so the guard does not fire on one.
- A tab that stops delivering frames is the common case. Pause deliberately on
  `visibilitychange` and keep the absorber for the cases that raise no event.

Related: [[clock-rebase-needs-a-live-anchor]],
[[driven-game-loop-needs-accumulator-reset]], [[animation-lifetime-in-frames]].
