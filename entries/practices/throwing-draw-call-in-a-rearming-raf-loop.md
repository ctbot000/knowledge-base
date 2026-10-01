---
title: An exception inside a self-rearming rAF callback truncates every frame without ever stopping the loop
tags: [browser, canvas, requestAnimationFrame, error-handling]
added: 2026-09-19
updated: 2026-10-01
sources:
  - https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-createradialgradient
  - https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-arc
  - https://webidl.spec.whatwg.org/#es-double
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

Canvas throws from two places, by different rules. `arc` and `ellipse` raise
`IndexSizeError` on a negative radius, but take a `NaN` or infinite argument
(radius included) silently, as `moveTo`, `fillText` and `drawImage` do. The
gradient factories (`createRadialGradient`, `createLinearGradient`,
`addColorStop`) take plain `double`s, so any non-finite argument, a centre as
much as a radius, raises `TypeError`, and a negative radius `IndexSizeError`.
So a `NaN` position from upstream (a perspective divide `1/(1 + z*k)` behind
the camera, a body that blew up) skips the shapes and throws at the first
gradient positioned on it.

## Why it matters

The symptom is a blank or half-drawn surface, which reads as a layout or
sizing problem, and the console fills with hundreds of identical errors that
nobody scrolls back to because the page is visibly alive. Buffered console
output also makes the errors look stale after a reload, so a fix appears not to
have worked.

## How to apply

- Clamp at the boundary rather than auditing call sites. A helper that
  guarantees a positive finite radius covers `arc` and `ellipse`:
  `const safe = Number.isFinite(r) && r > 0 ? r : 0.01;` A gradient also
  needs every coordinate checked with `Number.isFinite` before it is created.
- Guard perspective divides explicitly and skip anything behind the camera:
  `const d = 1 + z * k; if (d < 0.15) continue;`
- In a test, install `window.addEventListener('error', ...)` and assert the
  count is zero after exercising the full parameter range, rather than reading
  console output by eye.
- Related throttling failures from the other direction:
  [[animation-lifetime-in-frames]], [[ui-state-synced-only-in-raf]].
