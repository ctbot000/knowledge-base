---
title: A double-sided three.js material flips the normals of triangles wound away from the camera, hand-set normals included
tags: [three.js, webgl, shading, winding]
added: 2026-11-26
sources:
  - https://github.com/mrdoob/three.js/blob/dev/src/renderers/shaders/ShaderChunk/normal_fragment_begin.glsl.js
---

## Fact

`side: THREE.DoubleSide` does more than draw both faces: the fragment shader
multiplies the normal by -1 wherever `gl_FrontFacing` is false. A normal
attribute set by hand to face the viewer is turned away again on every triangle
whose winding disagrees with it. Checked on r187.

## Why it matters

Flat shapes built at run time (a triangulated section, a ribbon along a curve, a
decal) often mix windings: a triangulator picks its own, and a ribbon offset to
the other side of its curve reverses. With `DoubleSide` chosen precisely so that
winding would not matter, those pieces come out dark or unlit while their
neighbours are fine, and checking the normal attribute shows nothing wrong.

## How to apply

- Make the winding agree with the normals, or
- for a face that is only ever seen from one side, drop the flip:

```js
material.onBeforeCompile = (s) => {
  s.fragmentShader = s.fragmentShader.replace(
    '#include <normal_fragment_begin>',
    'vec3 normal = normalize(vNormal); vec3 nonPerturbedNormal = normal;');
};
```

The winding itself is [[backface-culling-deletes-geometry]]; settle it with
[[signed-volume-settles-winding]] on closed meshes.
