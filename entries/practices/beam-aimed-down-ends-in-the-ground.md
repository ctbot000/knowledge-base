---
title: A beam aimed from a raised muzzle at a target on the ground ends in the ground just past it
tags: [game-design, 3d, aiming]
added: 2026-11-07
---

## Fact

A straight line from hand height through the middle of a target on the floor
keeps going down. If the beam is cut at the first solid thing it meets, that is
the floor, a block or two past the target, however long its range.

## Why it matters

A shot that pierces or reaches far looks short and weak. The hits are worked out
separately, so everything along the line still takes damage, with no beam to be
seen reaching it. Nothing is wrong with the range or the raycast, so the tuning
gets looked at first. The nearer the target, the steeper the line and the worse
it looks.

## How to apply

Aim sideways at the target, but spread the drop in height over the whole range:

```js
const side = Math.hypot(aim.x - from.x, aim.z - from.z) || 1;
const dx = (aim.x - from.x) / side;
const dz = (aim.z - from.z) / side;
// Straight at one overhead; only down to its height by the far end otherwise.
const dy = (aim.y - from.y) / (aim.y > from.y ? side : range);
```

The line then passes a little over a near target's middle. Give the beam enough
width to cover that, and check it from the game's own camera at the shortest
range it can be fired at.
