---
title: A three.js Raycaster aimed from a camera before its first render uses the camera's stale world matrix
tags: [threejs, webgl, picking]
added: 2026-11-01
sources:
  - https://threejs.org/docs/#api/en/core/Raycaster.setFromCamera
---

## Fact

`Raycaster.setFromCamera` reads `camera.matrixWorld` (and the projection
matrix), not `position` and `quaternion`. Setting a camera's position, calling
`lookAt` or `OrbitControls.update()` changes only the local transform; the world
matrix is brought up to date by `renderer.render` (or `updateMatrixWorld`). A
pick made before the first frame — or after the camera moved but before the
next frame — casts from the old matrix: at startup, from the origin straight
down -z, which misses a ground plane entirely.

## Why it matters

A tap that comes right after a view opens (an automated test clicking at once,
a fast user, a page whose animation frames are throttled) silently picks
nothing, while the same tap a moment later works. It looks like a flaky test or
a lost event, not a stale matrix.

## How to apply

At the top of any picking function, bring the camera up to date first:

```js
camera.updateMatrixWorld();
// and if the canvas may have been resized since the last frame:
camera.aspect = canvas.clientWidth / canvas.clientHeight;
camera.updateProjectionMatrix();
raycaster.setFromCamera(ndc, camera);
```
