---
title: A dash blocked by a wall shows in its speed along the dash, not in its total speed
tags: [physics, collision, game-design]
added: 2026-11-03
---

## Fact

With collision resolved one axis at a time, a body dashing into a wall at an
angle loses only the part of its velocity that points into the wall and slides
along it at nearly full speed. A "stuck against a wall" test on total speed
never fires for it; the velocity component along the dash direction does drop.

## Why it matters

A charge meant to end in a bonk (and a stun the player can punish) instead
skids along the wall for its whole length, so the counterplay of dodging and
letting it hit the wall never works. Tests with a wall dead ahead pass, because
a head-on hit really does stop the body; only glancing hits slip through, and
in play almost every hit is a glancing one.

## How to apply

Measure progress along the dash, and require it to stay low for a moment so
the dash's first frames of acceleration and a step up a ledge do not count:

```js
const along = body.vx * dash.dirX + body.vz * dash.dirZ;
dash.stuck = along < dash.speed * 0.4 ? dash.stuck + dt : 0;
if (dash.stuck >= 0.12) bonk();
```

Test it with the wall at an angle to the dash, not only square on.
