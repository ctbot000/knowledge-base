---
title: Restitution measured at the bottom of a discrete overlap returns more energy than went in
tags: [simulation, physics, numerics]
added: 2026-09-22
---

## Fact

A fixed step overshoots a surface: the body is integrated past it and the
collision is detected on the next step, at depth `d`. Reflecting the velocity
measured *there* is wrong, because the body kept accelerating over that extra
depth. A position-correction pass then lifts it back to the surface without
removing the speed it gained falling into it, so every bounce adds about
`m * g * d` of energy.

With a 1/120 s step and an impact at 900 px/s the depth is ~7 px and the gain is
about 1.3% per bounce. A perfectly elastic ball climbs roughly 25% higher after
twenty bounces.

The correction is to reflect the speed the body had **at the surface**, by
discounting the gravity it picked up below it:

```js
const gn = Math.abs(dot(gravity, normal));
const submerged = penetration / approachSpeed + dt;   // + dt: this step's gravity
const atSurface = Math.max(0, approachSpeed - gn * submerged);
restitutionBias = restitution * atSurface;
```

## Why it matters

It looks like a restitution coefficient that is set too high, so it gets tuned
down — which hides it for one scene and leaves the energy gain in place for
every other. It is not a tuning error; the model is adding energy, and any
closed system built on it slowly heats up.

Halving the timestep halves the gain rather than removing it, so the fix looks
like it "nearly worked" and invites more of it.

## How to apply

- Discount both terms: the time spent below the surface (`d / v`) and the
  gravity already integrated into the velocity this step (`dt`).
- Prefer erring dissipative. A ball that loses half a percent per bounce reads
  as a real ball; one that gains reads as broken.
- Assert it directly: drop a ball with restitution 1 and check that it never
  rises above the height it was released from, over enough bounces to integrate
  the error.
