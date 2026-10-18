---
title: A three.js pass that redraws the scene through overrideMaterial sees the raw vertex attributes, not what each mesh's own shader does
tags: [threejs, webgl, postprocessing, ambient-occlusion]
added: 2026-10-18
sources:
  - https://threejs.org/docs/#api/en/scenes/Scene.overrideMaterial
  - https://github.com/mrdoob/three.js/blob/r186/examples/jsm/postprocessing/GTAOPass.js
  - https://github.com/mrdoob/three.js/pull/34831
---

## Fact

With `scene.overrideMaterial` set, every mesh is drawn with the override's own
vertex and fragment shaders. Whatever a mesh's `ShaderMaterial` did is skipped:

- **No `normal` attribute** (custom shaders often light from their own data): the
  override reads a zero normal, which normalizes to NaN.
- **Positions moved in the vertex shader** (instance offsets in a custom
  attribute, wind sway, packed coordinates) are drawn at the raw `position`.
- **Alpha-blended or alpha-tested cards** (blob shadows, decals, foliage) become
  solid quads, since the override ignores their maps and transparency.

GTAOPass (when it renders its own G-buffer), SSAOPass, SAOPass, BokehPass and
OutlinePass all build their normal, depth or mask buffers this way.

## Why it matters

The damage lands far from the cause. A voxel terrain with no normals turned the
whole ground and sky black under GTAO (the NaN goes through the blend), while the
ordinary models looked fine — it reads as a broken pass, not as missing data.

## How to apply

- Feed the pass the main render's depth instead of letting it re-render:
  render into a target with a `DepthTexture`, then `gtao.setGBuffer(depth)`;
  normals are reconstructed from depth, so every shader's own placement counts.
- In r186, passing `depthTexture` to the GTAOPass constructor throws; construct
  it without and call `setGBuffer` afterwards (fixed in r187).
- To check a pass, show its intermediate buffer (`gtao.output =
  GTAOPass.OUTPUT.Normal`) and look for black or missing regions.
