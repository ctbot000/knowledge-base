---
title: A WebGL canvas reads back blank except straight after drawing
tags: [webgl, canvas, screenshot, frontend]
added: 2026-10-12
sources:
  - https://registry.khronos.org/webgl/specs/latest/1.0/#2.2
---

## Fact

With `preserveDrawingBuffer: false` (the default), the drawing buffer is
cleared once a frame is handed to the compositor. `toDataURL`, `toBlob` or
`drawImage(webglCanvas)` return the picture only in the same task as the draw
calls; at any other time they give a blank (transparent or black) image.

## Why it matters

DOM-to-image screenshot libraries copy each `<canvas>` with `toDataURL` at
some later moment, so a 3D view comes out empty while the HTML around it is
fine. Turning `preserveDrawingBuffer` on to fix it costs performance on every
frame, not just when a picture is taken.

## How to apply

Take the 3D view yourself, in one task: render, then read back at once.

```js
renderer.render(scene, camera);
const scene3d = canvas.toDataURL('image/png');
```

For a whole-page screenshot, leave the WebGL canvas out of the DOM snapshot
(filter it, transparent background) and draw that snapshot over the image you
read back.
