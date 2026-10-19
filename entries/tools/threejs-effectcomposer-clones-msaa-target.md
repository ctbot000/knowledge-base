---
title: three.js's EffectComposer clones its render target, multisampling and all, for its second buffer
tags: [threejs, webgl, postprocessing, memory]
added: 2026-10-19
sources:
  - https://github.com/mrdoob/three.js/blob/r186/examples/jsm/postprocessing/EffectComposer.js
  - https://github.com/mrdoob/three.js/blob/r186/src/core/RenderTarget.js
---

## Fact

`new EffectComposer(renderer, target)` makes its second buffer with
`target.clone()`, and `RenderTarget.copy` carries `samples` and the depth
buffer. Hand it a multisampled target and both ping-pong buffers are
multisampled, though only the scene's own render gains anything from it; every
full-screen pass after that draws into, and resolves, a multisampled target.

## Why it matters

Multisampled storage is samples × (colour + depth) bytes per pixel: with 4×
MSAA and half-float colour, about 48 bytes per pixel, roughly 250 MB per buffer
on a 2880×1800 screen. Doubled, that is half a gigabyte of GPU memory for one
picture, which risks losing the context on phones and tablets.

## How to apply

- Draw the scene yourself into one multisampled target with a `DepthTexture`,
  then run the passes (`pass.render(renderer, write, read)`, swapping only when
  `pass.needsSwap`) between two plain targets, the last with
  `renderToScreen = true`.
- Or give the composer a target without samples and smooth edges afterwards
  (FXAA or SMAA, after the output pass, on sRGB values).
- Cap the post-processing resolution by a pixel count, not a fixed pixel
  ratio: memory and fill cost grow with the screen, not with the scene.
