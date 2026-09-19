---
title: The XZ plane seen from above is left-handed, so a yaw written as (cos, sin) is the mirror of a scene-graph rotation
tags: [3d, graphics, geometry, scene-graph]
added: 2026-09-20
---

## Fact

In a right-handed Y-up world, a rotation of `r` about `+Y` maps the local `+X`
axis to

```
(cos r, 0, -sin r)
```

because the rotation matrix about `+Y` carries `+X` toward `-Z`. But the
obvious way to place something "yawed by `y`" in the ground plane is to write a
2D circle in `(x, z)`:

```
right = (cos y, 0, sin y)
```

Those two differ by a reflection. Both are called yaw, both are a single
angle, and each is the natural expression in its own context — so a world
layout, a collision routine and a renderer can each be internally correct and
still disagree by a mirror.

The cause is that the `(x, z)` pair, viewed from `+Y`, is a **left-handed** 2D
frame. Ordinary 2D intuition about `(cos, sin)` silently flips a sign when it
is applied there.

## Why it matters

The symptom is geometry drawn in the wrong place, not geometry missing, so
nothing errors: the mesh exists, is positioned, is parented, is lit and is
drawn. A gate's crossbars rendered ninety degrees out from the uprights they
join, while the collidable gate stayed where the layout put it — you could fly
through a gate that was not where it looked.

Worse, the error is **invisible at exactly the angles anything gets checked
at**. At yaw 0 and yaw π the two expressions agree, so an axis-aligned test
object, a screenshot of the first item in a list, and any hand-placed
debugging case all look perfect. It only appears off-axis, where it reads as
"the artist rotated it wrong".

## How to apply

- Keep one conversion, in one place, and route every call site through it:
  `meshYaw(y) => -y` for a right-handed Y-up scene graph, alongside
  `rightVector(y)` and `facingVector(y)` used by the layout and the physics.
- Test it without a renderer: assert that the local `+X` direction implied by
  the scene-graph rotation equals the layout's right vector, over a spread of
  angles that **excludes** 0 and π, and separately assert that those two
  angles are the ones that hide it.
- When a rotation looks wrong, compare a derived direction vector rather than
  the angle. Two mirrored conventions print the same number.
- Related: [[mirrored-scale-inverts-rotation]], and
  [[yaw-derivatives-flip-with-the-yaw-axis]] for the same handedness trap where
  it reaches a physics table rather than a transform.
