---
title: To walk on worlds of any shape, take "up" from the shape's skeleton, not from its surface normal
tags: [geometry, sdf, games, camera, physics]
added: 2026-11-25
---

## Fact

Model a walkable body as a thin skeleton (a point, polyline, circle, disc, strip)
with a thickness round it, as a signed distance. The direction away from the nearest
skeleton point is then a gravity direction that turns smoothly right round the body
and exists off the ground too, while bumps, pits, ripples and props are added only to
the distance. The surface normal is used for collision alone.

## Why it matters

With up taken from the surface normal, every bump tilts the character and the camera,
a pit wall becomes a floor, and in the air there is no up at all. With a point-mass
centre, only spheres work: a ring, a plate or a ribbon pulls the player through its
hole or off its edge. The skeleton gives rings, plates (both faces, round a rounded
edge), tubes walked inside or out and even one-sided strips with the same few lines.

## How to apply

- Keep the player on the body they were on until another is clearly nearer
  (hysteresis), or up flickers between two bodies.
- Carry velocity and the camera's forward by the rotation from the old up to the new
  each step, so going straight round a ball stays straight.
- Distance checks that ignore up reach through thin bodies: for melee, blasts and
  slams also require the two ups to roughly agree.
- On a thin plate "towards the target" projected on the ground points nowhere when the
  target is on the other face; bots and reachability tests need to be told to cross
  the edge.
