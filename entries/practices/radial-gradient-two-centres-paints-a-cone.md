---
title: A canvas radial gradient with two different centres paints a cone, not a soft blob
tags: [canvas, graphics, frontend]
added: 2026-10-31
sources:
  - https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-createradialgradient
---

## Fact

`createRadialGradient(x0, y0, r0, x1, y1, r1)` interpolates between two
circles. When the centres differ and the start circle is not inside the end
circle, the gradient is a cone between them: filling a whole rectangle with it
paints a wedge or fan shape that runs off to the edge, not a round glow.

## Why it matters

Procedural textures often scatter soft blotches by calling the function with
fresh random numbers for each argument. Every blotch then becomes a sharp-edged
fan, and on a tiled or 3D surface the fans read as lighting or shadow artifacts
(faceted patches round objects), sending the debugging toward lights, shadow
maps or reflections instead of the texture.

## How to apply

For a soft round blotch, use one centre for both circles:

```js
const cx = rand() * w, cy = rand() * h, r = 60 + rand() * 90;
const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
```

Offset the inner centre only on purpose (a highlight off to one side), and keep
it inside the outer circle. When a 3D scene shows patches that survive turning
off the environment light and the shadows, look at the textures next.
