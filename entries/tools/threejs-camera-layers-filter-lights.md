---
title: A three.js camera set to some layers also leaves out every light not on them
tags: [three.js, webgl, layers, lighting, render-to-texture]
added: 2026-11-28
---

## Fact

`Object3D.layers` filters lights as well as meshes: while rendering, a light
whose layers share nothing with `camera.layers` is never collected, so it lights
nothing in that render (and casts no shadow). `renderer.compile` filters lights
the same way. Read in the r186 renderer's scene traversal, where the
`layers.test(camera.layers)` check comes before the `isLight` branch.

## Why it matters

The usual way to draw one object on its own (a character baked into a sprite, a
thumbnail, an outline pass) is to put it on a spare layer and render the whole
scene with a camera set to that layer only. With the scene's lights left on
layer 0, the object comes out unlit (black, or ambient only), which reads as a
material or colour-space bug rather than a layer one.

## How to apply

- Enable the spare layer on the lights the object should be lit by
  (`light.layers.enable(N)`), and disable it again when done.
- Use `layers.set(N)` on the object itself (and on everything added to it later)
  if the main camera must not draw it; `enable` keeps layer 0 too.
- A separate small scene with its own lights avoids the question, at the cost
  of moving the object between parents for each render.
