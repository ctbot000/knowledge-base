---
title: A path across a height field must be solved from the surface's own slope, not given a height of its own
tags: [procedural-generation, terrain, game-design, geometry]
added: 2026-09-12
---

## Fact

Laying a route over a surface by choosing its `(x, y)` shape and its height
separately gives you two independent functions of the same parameter. They agree
only by accident, and where they disagree the route becomes a causeway on stilts
or a trench — in one measured case 110 units above the ground on a 260-unit
mountain.

Solve the direction instead. On a surface whose fall-line slope is `g`, a step
that heads a fraction `fall` of the way into the fall line and spends the rest
across the slope has a grade of exactly `g · fall`. So for a wanted grade `G`:

```
fall = min(1, G / g)          # radial/uphill component of the unit step
side = sqrt(1 - fall²)        # across-slope component
```

Step by a fixed arc length along that direction and read the height from the
surface. The route now lies on the surface by construction, at the grade asked
for, and its length falls out of the geometry rather than being guessed.

## Why it matters

The stilts version looks fine from directly above and from far away, which is
where a generated world usually gets checked. It shows up as a wall beside the
path, as physics that cannot step onto it, or as a shadow with nothing casting
it — none of which point at the route generator.

The solved version also makes the design controllable: grade becomes an input,
and switchbacks come from flipping the across-slope sign while `fall` rises
briefly to 1.

## How to apply

- Never write the route's height. Read it from the field at the position you
  stepped to.
- `fall` is capped by 1, so a path can never be steeper than the surface's own
  fall line. Clamp it below that too, or a hairpin takes the fall line wherever
  the ground happens to be steepest and produces a pitch nothing can climb.
- Assert the result: sample the finished field along the route and check the
  measured grade against the one you asked for.
