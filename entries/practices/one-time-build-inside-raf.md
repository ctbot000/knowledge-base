---
title: One-time construction placed inside the rAF callback makes the first paint wait for a frame
tags: [browser, requestAnimationFrame, frontend]
added: 2026-09-18
---

## Fact

Building a scene lazily on the first animation frame is natural, because that is
the first moment the DOM is certainly laid out:

```js
function frame(now) {
  requestAnimationFrame(frame);
  if (!built) { build(); built = true; }   // measure, create nodes, first draw
  ...
}
```

Construction is now gated on a frame arriving, and a hidden or backgrounded
surface never delivers one. The page shows whatever its static HTML contained —
placeholder dashes, an empty chart — for as long as it stays hidden. That is
worse than a stalled update loop, because nothing exists to update.

## Why it matters

The failure is silent: no exception, no console output, no failed request.
Probing the model reports healthy values, because the model was never the
problem; only the DOM is empty. Every handler beginning `if (!built) return;`
takes that branch, so input is accepted and does nothing — the guard that looks
like defensive hygiene is what turns "not built yet" into "no error anywhere".

It is invisible in development, where the window is always focused, and it is
the normal case for a link opened in a background tab.

## How to apply

- Build eagerly; let the frame loop own only animation. Put the build behind an
  idempotent `ensureBuilt()` and call it at start-up, from any imperative
  render path, and at the top of `frame()`.
- If the geometry is not measurable yet, retry on a `setInterval` — timers keep
  firing where frames do not.
- Assert it: load the page and, before any frame can run, check that the nodes
  the build creates exist and carry real values.
- Related throttling from other angles: [[hidden-surface-delivers-no-frames]],
  [[ui-state-synced-only-in-raf]].
