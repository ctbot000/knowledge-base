---
title: Blending toward the nearest point on a path creases wherever the nearest point flips
tags: [graphics, terrain, geometry, procedural-generation]
added: 2026-09-12
---

## Fact

The usual way to stamp a path into a field is: find the closest point on the
polyline, take its value, blend by distance. The blend weight is continuous, but
the **value** is not: on the inside of a sharp corner there is a bisector where
the closest point jumps from one leg to the other, and the two legs hold
different values.

At a hairpin the two legs differ by whatever the path climbed around the corner,
so the stamped field gets a step of exactly that size running down the middle of
its own corridor. Everything looks correct until a corner is tight enough for
both legs to be inside one blend radius.

Averaging over *every* sample within range instead — `Σ w_i·v_i / Σ w_i`, with
`w_i` the same distance window — is continuous everywhere, and on a straight
stretch the symmetric weights reproduce the local value unchanged.

## Why it matters

The defect is invisible in the thing you are looking at: the path's own centre
line measures correct, the corner geometry is correct, and the surface normals
are smooth. What breaks is a narrow band a few units wide, so it is found by
something walking into it rather than by looking.

It generalises past terrain to anything stamped along a curve — a road's
material, a river's depth, a corridor's lighting, a brush stroke's width.

## How to apply

- Use a weighted average of all samples in range for the **value**, and the
  nearest-point distance only for the **weight**.
- Sample the path densely enough that several samples are always in range;
  spacing well under the blend radius is enough.
- To test it, walk the centre line and measure the field's gradient. A crease is
  a gradient jump that does not shrink when you halve the probe step — a genuine
  curvature does.
