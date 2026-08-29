---
title: An animation lifetime counted in frames never expires while rAF is throttled
tags: [animation, browser, requestAnimationFrame, frontend]
added: 2026-08-29
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
---

## Fact

`requestAnimationFrame` is not a clock. The browser throttles it heavily — or
stops it entirely — for hidden tabs, occluded windows, low-power modes and
embedded or snapshotting renderers.

So a particle written as `{ life: 120 }` and retired with `life-- > 0` does not
live for two seconds; it lives for 120 frames, however long the browser takes to
deliver them. When frames stop, the effect freezes on screen mid-flight and
stays there. Fixed per-frame physics (`y += vy`) fails the same way from the
other side: the motion is correct at 60 Hz, half speed at 30 Hz, and jumps a
visible distance after any stall.

## Why it matters

The frozen thing is usually an overlay — confetti, a flash, a transition veil —
drawn on top of the interface that the user has now returned to. It looks like a
rendering bug rather than a timing one, and it survives every interaction
because the code that would clear it is waiting on frames that are not coming.

It also hides during development, where the tab is always visible and focused,
and appears only for users who switch away mid-animation.

## How to apply

- End effects on wall-clock time, not frame count:
  `b.die = performance.now() + 2200`, retired with `now >= b.die`.
- Scale every per-frame increment by elapsed time, clamped so a long stall does
  not teleport anything: `const dt = Math.min(3, (now - last) / 16.67) || 1`.
- Reset the `last` timestamp when restarting an idle loop, or the first frame
  after the gap carries the whole pause as its delta.
- `document.visibilitychange` is the place to hard-clear an overlay if it must
  never outlive its animation.
