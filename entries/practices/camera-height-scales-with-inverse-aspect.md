---
title: In a width-scaled projection, camera height must scale with the inverse aspect ratio or a narrow viewport fills with near-field geometry
tags: [3d, camera, layout, graphics]
added: 2026-09-12
---

## Fact

A ground-plane renderer that scales both screen axes from the viewport width —
the usual way to keep a scene from stretching when the viewport shape changes —
has its nearest visible ground at

```
z_near = cameraDepth * cameraHeight * verticalScale / (height - horizonY)
```

`verticalScale` is proportional to width, so on a narrow, tall viewport the
numerator shrinks and the denominator grows. `z_near` collapses, and the closest
strip of ground the near plane admits expands to fill a third of the screen.

Scaling the camera height by `referenceAspect / aspect` cancels both terms
exactly and holds `z_near` constant at every viewport shape.

## Why it matters

The obvious fix for a stretched scene — scale both axes from one dimension — is
correct and introduces this second problem in the same change, so the shape that
was stretched is now merely empty. It reads as a level-of-detail or culling bug
rather than a camera one, because the geometry is all there and correctly drawn;
there is just a single huge polygon in front of everything.

Raising the camera is also the right answer aesthetically: a tall viewport wants
a more top-down view, which is what this produces for free.

## How to apply

- Derive it rather than tuning it. Write down `z_near` for your projection, then
  solve for the camera parameter that makes it independent of aspect.
- Clamp the result (roughly 0.85x to 2.6x the reference height) so an extreme
  viewport does not put the camera somewhere absurd.
- Anything positioned at a fixed fraction of the viewport height — the player's
  own vehicle, a reticle on the ground — must be re-derived from the projection
  too, or it floats off the surface as the camera moves.
- A near-plane cull leaves bare canvas under the closest drawn surface. The
  ground's edges are straight lines on a plane, so their projection is straight:
  extrapolate the nearest quad's edges to the bottom of the screen rather than
  widening the near plane.
