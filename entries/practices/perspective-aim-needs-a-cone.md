---
title: In a perspective view, a world-space proximity test rejects the target the player is aiming at
tags: [3d, game-design, input]
added: 2026-09-11
---

## Fact

When a 2D pointer aims into a 3D scene, the aim is a *ray* from the camera, and
the cursor's world position is only one point on it — wherever you chose to put
it. A hit test that measures world distance from that point therefore only works
at that one depth.

A target further down the ray sits directly under the crosshair on screen while
being metres away in world space, so a sphere around the cursor refuses the shot
the player just lined up perfectly. Widening the sphere does not fix it: it buys
depth tolerance by also accepting things the player is visibly not pointing at.

The test that matches what the player sees is angular — perpendicular distance
to the ray, against a radius that grows with distance:

```js
const t = dot(target - camera, rayDir);            // depth along the ray
const perp = length((target - camera) - rayDir*t); // off-axis distance
const hit = perp <= (radiusAtCursor / cursorDepth) * t;
```

## Why it matters

The complaint is "it misses when I'm clearly on it", which sounds like sloppy
collision or a lag problem, and both of those are worth ruling out first — so
the depth-dependence goes unnoticed while near targets keep working fine.

The inverse costs more. A cone that runs the depth of the scene is a long tube,
and everything in it is "aimed at", including whatever happens to be far behind
the target and too small to notice. If some of those are hazards, the player is
punished for a mistake they could not see.

## How to apply

- Use the angular test for aiming, and keep the cone's half-angle equal to the
  on-screen size of the reticle — that is the promise the crosshair makes.
- Resolve a swing or shot to the *single* best-aimed candidate, ranked by
  off-axis distance relative to each candidate's own allowance, rather than
  taking everything the cone contains.
- Bound the cone's depth to the range the player can actually read.
- Test with a target at the far plane, not at the cursor's own depth; that is
  the only place the two models disagree.

Related: [[framing-a-box-is-a-per-corner-solve]].
