---
title: Where something rests on a model is the highest point under its footprint, not the hit of a ray through its centre
tags: [3d, graphics, geometry, testing]
added: 2026-10-03
---

## Fact

A thing set down on a model — a bird on a head, a hat on hair, a prop on a
shelf — rests on the highest point under its whole footprint. One ray cast
down through its centre measures something else: on any top with gaps (spiky
hair, curls, two leaves either side of a stem) the centre ray falls into a gap
and reads low, by a good share of the feature's height.

## Why it matters

Attachment heights are usually tuned by eye once and stored as constants, then
drift as the models change; the drift shows only as a prop sunk into, or
hovering over, one combination out of dozens. Calibrating them with a centre
ray fails the other way: the number looks precise and puts the prop inside the
spikes.

## How to apply

- Sample a disc of rays the radius of the resting thing's footprint (a ring or
  two of 8–12 rays, plus the centre) and take the highest hit.
- Size the disc to the footprint, not larger: a wider one picks up what the
  thing sits beside rather than on, such as a bow at the side of a head.
- Keep stored heights honest with a test over every combination of model,
  accessory and style. In three.js, `Raycaster.intersectObject` works headlessly
  in Node with no WebGL context, so assert `0 <= stored - measured <= tolerance`
  for each one.
- Exclude by name what the thing is known to sit beside, so the test stays
  strict for everything else.
