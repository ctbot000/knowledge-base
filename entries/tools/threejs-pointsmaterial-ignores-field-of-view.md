---
title: three.js sizes PointsMaterial points without the camera's field of view, so a narrow lens shrinks them
tags: [three.js, webgl, particles, camera]
added: 2026-11-26
sources:
  - https://github.com/mrdoob/three.js/blob/dev/src/renderers/shaders/ShaderLib/points.glsl.js
  - https://github.com/mrdoob/three.js/blob/dev/src/renderers/webgl/WebGLMaterials.js
---

## Fact

With `sizeAttenuation` (the default), a point's size on screen is
`size * (height / 2) / distance`. The projection matrix is not in it. A mesh of
the same world size covers `size * (height / 2) / (distance * tan(fov / 2))`,
so a point matches its world size only at a 90° field of view. At 50° it is
drawn 2.1 times too small, at 22° 5.1 times. Checked on r187.

## Why it matters

Particles tuned with one lens turn into one-pixel specks with a longer one,
the kind used for product shots, portraits and diagrams, and it reads as a
missing texture, an alpha problem or depth fighting. A camera that zooms by
changing `fov` leaves its particles behind at their old size.

## How to apply

- Multiply the size by `1 / tan(fov / 2)`:
  `material.size = world / Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2)`,
  and again whenever the field of view or `zoom` changes.
- `height` is the renderer's whole drawing buffer, not the viewport, so a point
  in a scissored half-height view is twice too big for that view.
