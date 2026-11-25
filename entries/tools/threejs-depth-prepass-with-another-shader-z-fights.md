---
title: A depth-only prepass for a see-through three.js model z-fights with it unless pushed back, because another vertex shader rounds differently
tags: [three.js, webgl, transparency, z-fighting, depth]
added: 2026-11-26
sources:
  - https://threejs.org/docs/#api/en/materials/Material.polygonOffset
---

## Fact

An additive or transparent model shows every surface inside and behind it, so
overlapping parts pile up into a white blob. Drawing it first with
`colorWrite: false` leaves only its nearest surface visible. But if that prepass
uses a built-in material and the visible pass a `ShaderMaterial`, the two vertex
shaders multiply their matrices in a different order
(`projection * modelView * p` against `projection * (view * (model * p))`), the
depths differ in the last bits, and the model comes out in camouflage patches.

## Why it matters

`depthFunc` is already `LessEqualDepth`, so equal depths would pass; it looks as
if the prepass were broken or the pattern came from the shader's own noise. The
patches also move with the camera, like a lighting bug.

## How to apply

Push the prepass back a little, or make both passes compute the position with
the very same expression:

```js
const near = new THREE.MeshBasicMaterial({
  colorWrite: false, transparent: true,       // transparent: same queue as the model
  polygonOffset: true, polygonOffsetFactor: 1.5, polygonOffsetUnits: 4,
});
const front = new THREE.Mesh(mesh.geometry, near);
front.renderOrder = 1;
mesh.renderOrder = 2;
mesh.add(front);
```

`renderOrder` matters: all of the prepass has to be drawn before any of the
visible pass, or parts of one model still show through each other.
