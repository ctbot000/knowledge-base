---
title: A node mirrored with a negative scale also mirrors every rotation applied beneath it
tags: [3d, animation, scene-graph]
added: 2026-09-11
---

## Fact

Mirroring the right half of a symmetric rig by setting one axis of a parent's
scale to `-1` is the standard trick: build one wing, one arm, one fin, and
reuse it. The mirror applies to the animation too.

Scale is applied inside the node's own transform, before its rotation, so a
point the mirror moved to `-z` is then swept the *other way* by the same
rotation. Driving both sides from one value therefore separates them:

```js
left.rotation.x  = angle;   // tip rises
right.rotation.x = angle;   // tip drops — the mirror flipped the sense
```

The rig is symmetric at rest, so it looks correct until the first frame of
animation. Then the two halves move apart and stay apart.

## Why it matters

The shape it produces — one wing up, one down, forever — reads as a broken
model or a bad export, so the search starts in the geometry rather than in the
one line that drives both sides from a single number. Nothing is wrong with the
mesh, and the rotation value is the one intended.

It also survives review, because the symmetry that makes the bug is exactly the
symmetry that makes the code look right.

## How to apply

- Record which side a mirrored node is on when you build it, and cancel the
  mirror where the animation is applied: `node.rotation.x = angle * node.side`.
- Prefer a rotation offset over a negative scale when the rig will be animated —
  place the second copy by rotating it 180 degrees about the body axis, and the
  sense is preserved.
- A negative scale also flips winding, so backface culling and normals invert
  with it; a mirrored part that renders inside-out is the same cause.
- Check a rig on the first animated frame, never at rest — rest is the one pose
  where this is invisible.
