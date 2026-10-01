---
title: Every canvas starts with a 300 by 150 bitmap, so a nonzero width does not mean it was drawn
tags: [canvas, testing, browser]
added: 2026-10-02
sources:
  - https://html.spec.whatwg.org/multipage/canvas.html#attr-canvas-width
---

## Fact

A `<canvas>` without `width` and `height` attributes has a transparent 300 by
150 bitmap from the moment it exists, and `canvas.width` reads 300. CSS sizing
only scales that bitmap. The size changes only when code assigns it, typically
in the app's first draw.

## Why it matters

A test that waits for `canvas.width > 0` to know the app has drawn waits for
nothing. The condition is true at once, and the pixel read after it comes back
transparent black whenever the first draw is late: a slow first frame under
software rendering, or a frame loop that has not ticked yet. So it passes on
fast machines and fails intermittently on CI.

The same assumption hides in guards such as `c.width ? read(c) : null`, whose
null branch never runs.

## How to apply

- Wait for something the draw itself sets: the size the app assigns (a square
  canvas is never 300 by 150, so `width === height`), a pixel, or a flag the
  app exposes.
- If "not drawn yet" should be observable, declare `width="0" height="0"` in
  the markup and let the first draw size the canvas.
- Assigning the size also clears the canvas:
  [[resizeobserver-first-callback-clears-the-canvas]].
