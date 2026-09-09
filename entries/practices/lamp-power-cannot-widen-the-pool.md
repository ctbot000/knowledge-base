---
title: Brightening a lamp cannot widen the pool of light on a wall of coplanar faces
tags: [graphics, lighting, webgl]
added: 2026-09-09
---

## Fact

With standard diffuse shading, a surface's brightness carries a `max(dot(N, L),
0)` factor. On a wall whose faces all share one normal, that factor is fixed by
geometry: a point at distance `r` along the wall from a lamp standing `h` off it
sees `N·L = h / sqrt(r² + h²)`, which collapses toward zero as `r` grows no
matter how much power the lamp has.

So the lit region is a disc whose radius is set by `h`, not by intensity.
Turning the lamp up scales every pixel, which means the centre clips to white
long before the edge becomes visible.

## Why it matters

The symptom — a blown-out hotspot surrounded by black — reads as "the lamp is
too strong" and "the lamp is too weak" at the same time, so tuning oscillates
between the two and neither setting looks right. The attenuation curve gets
blamed, and rewriting it does not help, because attenuation is not the term that
is killing the edge.

It is common in exactly the scenes where it is least expected: a tile wall, a
facade, a floor plane, anything ported from a flat 2D renderer where every
surface was simply filled.

## How to apply

- Move the light **off the surface along its normal**. Doubling `h` roughly
  doubles the radius at which `N·L` still contributes; it is the only lever with
  the right shape.
- Wrap the diffuse term so the terminator is soft rather than hard:
  `ndl = max((dot(N, L) + w) / (1.0 + w), 0.0)` with `w` around 0.25-0.5. This
  is the cheap stand-in for the bounce light a flat wall would really receive.
- Add a highlight roll-off (`c / (1 + k*c)`) so raising power stops clipping and
  starts reaching further.
- Check the fix at the edge of the intended radius, not at the centre. The
  centre looks correct under every wrong setting.
