---
title: Setting glslVersion GLSL3 on a three.js ShaderMaterial removes the gl_FragColor its own chunks write to
tags: [threejs, webgl, glsl]
added: 2026-10-01
sources:
  - https://github.com/mrdoob/three.js/blob/dev/src/renderers/webgl/WebGLProgram.js
---

## Fact

three.js compiles every non-raw `ShaderMaterial` as `#version 300 es` already,
with `gl_FragColor` defined to a declared `pc_fragColor` output. Setting
`glslVersion: THREE.GLSL3` upgrades nothing: it only drops those two lines and
expects you to declare your own `out vec4`. Chunks such as
`#include <colorspace_fragment>` still assign to `gl_FragColor`, so the fragment
shader fails with "'gl_FragColor' : undeclared identifier" and
"'linearToOutputTexel' : no matching overloaded function found".

## Why it matters

GLSL3 is usually set to get `sampler2DArray`, `texture()` or integer
attributes, which work without it. The broken material draws nothing while
every other material renders, so it reads as missing geometry; the only trace
is a shader error logged once and a stream of "useProgram: program not valid"
warnings.

## How to apply

- Leave `glslVersion` unset on `ShaderMaterial`; GLSL ES 3.00 features are
  already available, and `attribute`/`varying` map to `in`/`out` by define.
- Set `THREE.GLSL3` only on a `RawShaderMaterial`, or when the shader declares
  its own output and includes no chunk that writes `gl_FragColor`.
