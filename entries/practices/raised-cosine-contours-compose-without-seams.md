---
title: A raised-cosine contour is flat at its own rim, so contours sum into a height field with no creases
tags: [graphics, terrain, simulation, game-design]
added: 2026-09-09
---

## Fact

For a radial bump of amplitude `A` and radius `R`,

```
h(d) = A * 0.5 * (1 + cos(pi * d / R))     for d < R, else 0
```

is zero at `d = R` **and** has zero derivative there. So it drops into the
surrounding ground with matching value and matching slope, and any number of
these can be added together in any arrangement without a crease at any rim.

The obvious alternatives do not have that property. A linear cone
`A * (1 - d/R)` matches in value but arrives at the rim with a finite slope,
leaving a visible ring and — in a simulation — a step change in force. A
plateau matches in neither and is a cliff.

Steepest slope is `A * pi / (2R)`, at `d = R/2`. That one number is the thing to
constrain, not the amplitude.

## Why it matters

A height field is usually assembled from primitives, and "the pieces line up" is
naturally checked on value alone, because that is what is visible in a still
frame. Slope discontinuities show up later and elsewhere: as a shading seam that
looks like a normals bug, and as an impulse that flicks a moving body sideways
for no reason the code can be seen to contain.

The bigger payoff is structural. If the surface is smooth everywhere, a body can
be glued to it — position on the plane, height read from the field — and there
is no edge to leave. That removes airborne physics, landing detection and the
whole class of bugs where something ends up under the terrain.

## How to apply

- Gradient is radial, magnitude `-A * 0.5 * (pi/R) * sin(pi * d / R)`; split it
  by `(dx/d, dy/d)`, and use zero at `d = 0` rather than dividing by it.
- With a body glued to the surface, downhill acceleration is `-g * gradient`.
  Assert `g * steepest_slope < friction_deceleration`, or a body can accelerate
  downhill for ever.
- Contours add, so the combined gradient can exceed every individual one.
  Measure the assembled field over a grid; do not trust the per-primitive number.
- Check that goal positions — a cup, a spawn, a resting place — sit where the
  gradient is near zero, or nothing will settle there.
