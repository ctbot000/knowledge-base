---
title: A ResizeObserver's first callback wipes whatever the canvas has already drawn
tags: [canvas, browser, frontend]
added: 2026-09-21
sources:
  - https://html.spec.whatwg.org/multipage/canvas.html#concept-canvas-set-bitmap-dimensions
  - https://drafts.csswg.org/resize-observer/#intro
---

## Fact

`ResizeObserver` delivers one observation as soon as an element is observed —
the element need not change size — and that callback lands asynchronously,
after the synchronous setup around it has finished.

Assigning `canvas.width` resets the bitmap to transparent black *and* resets
every context property (transform, `fillStyle`, `lineWidth`, clip), even when
the assigned value is identical to the current one. So the usual arrangement
paints and is then silently erased a tick later:

```js
new ResizeObserver(resize).observe(canvas);   // fires once, on its own
resize();                                     // sets canvas.width
draw();                                       // this frame does not survive
```

## Why it matters

While frames are being delivered the loss is invisible — the next one repaints
within 16 ms. It shows only where there is no next frame: a background tab, an
occluded window, a snapshotter, an embedded preview pane, or a loop paused
while off-screen. The canvas then stays blank and reads as a broken draw path
rather than a lost one, because every pixel readback agrees it is empty.

## How to apply

- Make the resize handler idempotent, and let it repaint what it destroyed:
  compare the computed pixel size against `canvas.width`/`canvas.height`,
  return early when unchanged, and call the draw function right after any
  assignment that did happen.
- Never treat "already drew once" as a reason to skip drawing after a resize;
  the resize is what undid it.
- CSS `width`/`height` only scale the bitmap and do not clear it. The attribute
  and the property both do.
