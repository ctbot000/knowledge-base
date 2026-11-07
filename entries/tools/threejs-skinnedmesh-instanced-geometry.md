---
title: A three.js SkinnedMesh can draw an InstancedBufferGeometry, every instance in one draw call
tags: [three.js, webgl, skinning, instancing, fur]
added: 2026-11-07
---

## Fact

`InstancedMesh` cannot be skinned, but a plain `SkinnedMesh` given an
`InstancedBufferGeometry` can: the renderer draws `geometry.instanceCount`
copies of the skinned shape in one draw call, and the vertex shader tells them
apart by an instanced attribute. Seen working on r186.

## Why it matters

Shell fur, outlines and other "the same deformed skin N times" effects look as
if they need N skinned meshes, one draw call each, or a merged geometry N times
the size. Neither is needed.

## How to apply

- Build the geometry from the skinned one's own attributes
  (`g.setAttribute(name, base.attributes[name])`), add an
  `InstancedBufferAttribute` such as a layer height, and read it in
  `#include <begin_vertex>` so the offset is applied before skinning.
- Several meshes can share the geometry at different counts: set
  `geometry.instanceCount` in the mesh's `onBeforeRender`, which runs just before
  its draw. A count of 0 draws nothing.
- To drop layers from the end of the list and keep the rest evenly spread, store
  heights in a low-discrepancy order (`(i * 0.618...) % 1`), not root to tip.
- Give the mesh `boundingSphere` and `boundingBox` yourself. Otherwise the first
  frustum test or `Box3.setFromObject` walks every vertex through its bones.
- Keep the layered mesh out of the shadow pass, and let a plain skinned mesh of
  the same shape cast the shadow.
