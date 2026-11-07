---
title: A creature sculpted from melted distance fields has one seamless skin, and its bone weights come from the same parts
tags: [procedural, modelling, sdf, surface-nets, skinning]
added: 2026-11-07
---

## Fact

Primitives parented to bones always show where a leg meets a body. Define the
same parts as distance functions (round cones, ellipsoids) joined by a smooth
minimum, wrap one mesh over them with Surface Nets, and the joins blend the way
clay does. Each part's own distance at a vertex then gives that vertex's bone
weights: `exp(-max(d, 0) / reach)`, summed per bone, keeping the top four.

## Why it matters

Changing proportions becomes changing numbers, so one sculpting function yields
many very different animals without any modelling. Skinning also needs no
painting, and needs none of the mesh's topology to be known in advance.

## How to apply

- Keep the parts small in number, and skip any part further away than the current
  distance plus its blend width: the smooth minimum cannot reach past that.
- Measure only near the surface: test a block's centre, and fill the block with
  that value when the distance exceeds its half diagonal. Mirror the grid for
  symmetric bodies. A whole body then takes tens of milliseconds at runtime.
- Use a rectilinear grid with non-uniform lines to spend vertices on heads and
  paws. Normals come from the field's gradient, so they stay smooth on a coarse
  grid.
- Thin plates such as ears need cells thinner than the plate, or they come out
  ribbed. Build those as a parametric sheet instead and still take their normals
  from the field.
- Stop a part pulling the wrong side by zeroing its weight on the far side of the
  midline. Tagging parts (leg, muzzle, ear) also gives you markings and fur length
  per vertex.
