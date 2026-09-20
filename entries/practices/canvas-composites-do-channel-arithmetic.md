---
title: Canvas blend modes do per-channel set arithmetic, so several soft masks fit in one RGBA upload
tags: [canvas, graphics, frontend]
added: 2026-09-20
sources:
  - https://www.w3.org/TR/compositing-1/
---

## Fact

`globalCompositeOperation` with a pure primary colour edits one channel and
leaves the rest alone, which makes 2D canvas a usable mask compositor:

```js
ctx.fillStyle = '#000'; ctx.fillRect(0, 0, w, h);   // opaque, so ab = 1

ctx.globalCompositeOperation = 'lighter';           // ADD into a channel
ctx.fillStyle = '#ff0000'; fill(faceOval);          //   -> red
ctx.fillStyle = '#00ff00'; fill(lips);              //   -> green

ctx.globalCompositeOperation = 'multiply';          // SUBTRACT from a channel
ctx.fillStyle = '#00ffff'; fill(lips); fill(eyes);  //   -> clears red only
```

Over an opaque destination the compositing formula reduces to
`Co = as·B(Cb,Cs) + (1-as)·Cb`, so `multiply` by `(0,1,1)` scales red by the
source's alpha and leaves green and blue untouched — and a `ctx.filter =
'blur(Npx)'` on each fill turns that into a *proportional* contribution, giving
feathered edges instead of a stair-step.

"The face oval, minus eyes, brows and lips" is therefore two draws, and three
independent soft masks reach the GPU as one RGBA texture.

## Why it matters

Subtraction is the operation people assume canvas cannot do, so the region gets
approximated with a hand-shrunk polygon that never quite matches, or the masks
get rasterised into typed arrays on the CPU, or each one becomes its own
texture — more uploads, more samplers, more state to keep in sync per frame.

## How to apply

- Fill the destination opaque first. The reduction above assumes `ab = 1`;
  over transparent pixels the same draws give premultiplied surprises.
- Additive passes first, subtractive passes second.
- Leave alpha out of the packing and keep the texture opaque — three channels
  is usually enough, and analytic falloffs in the shader can carry anything
  that is just a soft radial blob.
- Read a channel back and assert its value at a few known points; the failure
  mode is a channel that is silently zero everywhere.
