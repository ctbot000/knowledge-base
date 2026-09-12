---
title: A renderer's colour management ends at its materials, so a hand-written shader writes linear values to an sRGB buffer
tags: [graphics, webgl, color, rendering]
added: 2026-09-12
sources:
  - https://threejs.org/docs/#manual/en/introduction/Color-management
---

## Fact

A linear-workflow renderer converts every colour you author into a linear
working space on the way in and encodes back to sRGB on the way out. That
encode is emitted **into material shaders**, not into a fragment shader you
wrote yourself.

So a custom shader that writes an authored colour straight out —
`gl_FragColor = vec4(mix(horizon, zenith, k), 1.0)`, both uniforms — puts
linear values into an sRGB buffer. Each colour lands at its own linear form: a
mid-blue `#2f78cc` renders as `#07309a`, a neutral `#808080` near `#373737`.

## Why it matters

It comes out uniformly too dark rather than obviously broken, so it reads as
"these colours were badly chosen" or "the lighting is wrong", and the fix gets
attempted in the palette or the light rig. Neither can work: the error is one
fixed transfer function applied to every value, and re-picking colours against
it bakes it permanently into the data. The lit geometry beside it looks
correct, which argues against a pipeline-wide cause and sends the search
somewhere else again.

## How to apply

- Encode at the end of your own fragment shader, or use the engine's chunk
  where one exists — three.js has `#include <colorspace_fragment>`, available
  to `ShaderMaterial` but not to `RawShaderMaterial`:

  ```glsl
  vec3 toSRGB(vec3 c) {
    return mix(c * 12.92, 1.055 * pow(c, vec3(0.41666)) - 0.055,
               step(vec3(0.0031308), c));
  }
  ```

- Identify it by the number, not by eye: a rendered value near
  `(authored/255)^2.2` is the missing encode, not the palette.
- It applies to every colour-valued uniform you consume, and in reverse to
  anything you sample and hand back.

Related: [[palette-is-calibrated-to-its-shading-model]].
