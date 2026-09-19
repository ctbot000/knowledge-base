---
title: A retirement sweep placed after an activity guard stops running exactly when there is nothing happening
tags: [simulation, state, debugging]
added: 2026-09-19
---

## Fact

Buffers of time-limited things — decals, trails, particles, toasts, cached
tiles — usually get appended and retired in one function, and that function
usually opens with a guard so it does no work when nothing is happening:

```js
function record(dt) {
  if (cooldown > 0 || speed < THRESHOLD) return;   // nothing to add
  buffer.push({ ..., expires: clock + LIFETIME });
  while (buffer.length && buffer[0].expires < clock) buffer.shift();   // never reached
}
```

The retirement is correct and never runs while the guard holds. Items then
persist for as long as the system stays idle, however far past their expiry.

## Why it matters

The idle state is precisely when the stale items are on screen and being looked
at. A driver who stops and turns around sees the tyre marks that should have
faded minutes ago; a paused editor keeps its transient highlights; a buffer that
should be bounded grows until the *next* burst of activity trims it.

Every part reads as correct in isolation: the lifetime is set, the comparison is
right, the guard is sensible. Only the order is wrong, so the bug survives code
review and any test that keeps the system busy.

## How to apply

- Retire first, unconditionally, before any early return. It is cheap, it is
  idempotent, and it is the only ordering that holds in every state.
- Better, separate the two responsibilities: a `retire()` called from the step
  function and an `append()` that the guard may skip.
- Assert it where it actually breaks — bring the system to rest, advance the
  clock past the lifetime, and check the buffer, rather than checking it while
  things are still being added.
- Related: [[animation-lifetime-in-frames]],
  [[retention-window-scales-with-observer-speed]].
