---
title: An exception inside a self-rearming rAF callback truncates every frame without ever stopping the loop
tags: [browser, canvas, requestAnimationFrame, error-handling]
added: 2026-09-19
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/createRadialGradient
---

## Fact

The recommended shape for a frame loop schedules the next frame before doing
any work, so a slow or failing frame cannot kill the animation:

```js
function frame(now) {
  requestAnimationFrame(frame);   // re-arm first
  draw(now);                      // anything here may throw
}
```

That resilience has a cost nobody plans for. If `draw` throws partway through,
every subsequent frame throws at the same place. The loop runs for ever, the
page stays responsive, input still works, and the canvas is left holding
whatever had been painted before the throwing call — often just the background.

Canvas is unusually easy to throw from, because it validates geometry:
`createRadialGradient` and `arc` raise `IndexSizeError` on a negative or
non-finite radius. Any radius computed from simulation state can get there — a
wave term mapped to the wrong range, a perspective divide `1/(1 + z*k)` for a
body that drifted behind the camera, a `NaN` from anywhere upstream.

## Why it matters

The symptom is a blank or half-drawn surface, which reads as a layout or
sizing problem, and the console fills with hundreds of identical errors that
nobody scrolls back to because the page is visibly alive. Buffered console
output also makes the errors look stale after a reload, so a fix appears not to
have worked.

## How to apply

- Clamp at the boundary rather than auditing call sites. One helper that
  guarantees a positive finite radius removes the whole class:
  `const safe = Number.isFinite(r) && r > 0 ? r : 0.01;`
- Guard perspective divides explicitly and skip anything behind the camera:
  `const d = 1 + z * k; if (d < 0.15) continue;`
- In a test, install `window.addEventListener('error', ...)` and assert the
  count is zero after exercising the full parameter range, rather than reading
  console output by eye.
- Related throttling failures from the other direction:
  [[animation-lifetime-in-frames]], [[ui-state-synced-only-in-raf]].
