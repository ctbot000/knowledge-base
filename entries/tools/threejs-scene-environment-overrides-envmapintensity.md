---
title: A three.js material lit by scene.environment ignores its own envMapIntensity
tags: [threejs, webgl, pbr, environment-map]
added: 2026-10-19
sources:
  - https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js
  - https://threejs.org/docs/#api/en/scenes/Scene.environmentIntensity
---

## Fact

When a Standard, Physical, Lambert or Phong material has no `envMap` of its own
and the scene has `scene.environment`, the renderer overwrites that material's
`envMapIntensity` uniform with `scene.environmentIntensity` on every draw
(three r163 and later). The material's own `envMapIntensity` is never read.

## Why it matters

Per-material reflection strength silently stops working: glossy eyes and satin
fur reflect the same amount, and tuning the number on the material changes
nothing, which reads as a broken environment map or a wrong roughness.
`scene.environment` also reaches Lambert and Phong materials as a reflection,
changing materials that were never meant to be part of it.

## How to apply

- To keep per-material strengths, assign the texture to each material's own
  `envMap` (keep a registry of the materials you make) and leave
  `scene.environment` unset.
- To dim them all together (night), use one shared uniform injected in
  `onBeforeCompile`, e.g. replace `* envMapIntensity` with
  `* envMapIntensity * uShared` in `envmap_physical_pars_fragment`.
- One global strength for everything is the only case `scene.environment` with
  `scene.environmentIntensity` handles as written.
