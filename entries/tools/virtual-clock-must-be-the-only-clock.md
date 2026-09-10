---
title: A virtual clock has to be the only clock, or what it drives never moves
tags: [testing, automation, animation, game-loop]
added: 2026-09-11
---

## Fact

Adding a way to step time — a test hook, a replay, a timeline scrubber —
introduces a second clock. Anything that still calls `performance.now()`
directly is stamping events on the real timeline while the stepper advances a
different one, and the two drift apart immediately.

The usual result is an animation that never starts. A tween records
`start = performance.now()`, the stepper advances from a baseline captured
before that, elapsed time comes out negative, and the obligatory
`clamp(elapsed / duration, 0, 1)` pins progress at zero. Stepping further does
not help; the baseline is behind the start and stays behind it.

## Why it matters

Nothing fails. The tween object exists, the step call returns, the frame is
drawn, and the state does not change — so it reads as "the animation was never
wired up" and sends you into the code that creates it, which is correct.

The opposite drift is worse, because it half-works: when the stepper is *ahead*
of the recorded start, progress clamps to 1 on the first step, the animation
completes instantly, and the final state is right. Every assertion about the
outcome passes and only the motion is missing, so the harness certifies an
animation it never actually ran.

## How to apply

- Express the virtual clock as an offset on the real one and route every reader
  through it, the code that records start times included:

  ```js
  let offset = 0;
  const clock = () => performance.now() + offset;
  const step = (ms) => { offset += ms; advance(clock()); render(); };
  ```

  A stepped clock and a real frame then cannot disagree about "now".
- Step by moving the offset, not by passing a chosen timestamp into `advance`.
  A caller-supplied timestamp is a second source of truth and will diverge.
- After adding the hook, grep for remaining direct `performance.now()` and
  `Date.now()` calls. The ones you miss are precisely the bug.
- Progress stuck at 0, or jumping straight to 1, is the signature — a genuinely
  wrong animation moves, it just moves wrongly.

Related: [[driven-game-loop-needs-accumulator-reset]],
[[animation-lifetime-in-frames]], [[hidden-surface-delivers-no-frames]].
