---
title: A three.js light's shadow camera ignores the bounds you assign until updateProjectionMatrix is called
tags: [threejs, webgl, shadows]
added: 2026-09-12
sources:
  - https://threejs.org/docs/#api/en/lights/shadows/DirectionalLightShadow
---

## Fact

`DirectionalLightShadow` is constructed with an `OrthographicCamera(-5, 5, 5,
-5, 0.5, 500)`. Assigning `light.shadow.camera.left/right/top/bottom/near/far`
changes those *properties* and nothing else: `LightShadow.updateMatrices()` runs
every frame and rebuilds the camera's **view** matrix from the light's position,
but never its **projection** matrix.

So a shadow volume "widened" to cover a scene silently stays 10x10 units.

The second half is what makes it destructive. `shadow.normalBias` is measured in
world units and is normally sized against the texel size of the box you intended
(`2 * extent / mapSize`). Against the 10x10 box that is actually in force, that
same value is hundreds of texels, so every lookup samples far outside the map and
large regions come back shadowed.

## Why it matters

The symptom is not "shadows are the wrong size" — it is broad, hard-edged dark
patches across geometry nowhere near the caster, which reads as a lighting or
material bug. The shadow configuration is right there in the source looking
correct, and every value in it is the value you set.

It also survives a code review, because the fix is a call that is not in the code
rather than a wrong value that is.

## How to apply

- Call it yourself, immediately after setting the bounds:

  ```js
  Object.assign(light.shadow.camera, { left: -e, right: e, top: e, bottom: -e });
  light.shadow.camera.updateProjectionMatrix();
  ```

- Size the biases against the box that is really in force:
  `const texel = 2 * extent / light.shadow.mapSize.width`, then
  `normalBias ≈ 2 * texel`.
- Any camera whose `left/right/top/bottom/near/far` are changed after
  construction needs the same call; three only rebuilds projections for the
  cameras it owns end to end.
