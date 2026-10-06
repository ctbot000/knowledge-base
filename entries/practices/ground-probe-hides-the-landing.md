---
title: A ground probe that marks a falling body grounded before contact hides the landing from anything keyed on the airborne flag
tags: [game-design, collision, simulation]
added: 2026-10-06
---

## Fact

Character controllers often set `onGround` whenever the feet are within a small
tolerance `ε` above a surface, so walking and jumping stay stable. A body
falling at speed `v` with substep `h` ends some substep inside that band with
probability about `ε / (v·h)` (capped at 1). The next substep's contact is then
handled as a grounded body resting, not as a landing: an impact event guarded
by `if (!onGround)` never fires, and a jump input checked against `onGround`
fires from mid-fall instead. With `ε = 0.05` and `h = 1/90 s`, about 40% of
landings from one to eight units up reported no impact.

## Why it matters

Landing feedback (a thump, a dust puff, fall damage) is skipped on a large,
height-dependent share of landings. It is intermittent, so it reads as an audio
or effects glitch rather than a physics one.

Anything that redirects the impact suffers worse. A bounce pad keyed on the
airborne-to-grounded transition loses its bounce about half the time, and with
jump held the standing-jump branch takes over, replacing the speed carried
down with a standing jump's, so a "higher each bounce" mechanic resets at
random.

## How to apply

- Key impact logic on the contact's own normal speed (faster than one substep
  of gravity gives a resting body), not on the grounded flag left by the
  previous substep.
- In the jump-from-ground path, check whether the body is still moving down:
  inside the probe band it is landing, and that fall speed belongs to the
  impact.
- Test by dropping from a sweep of fractional heights and counting reported
  landings; every drop must report one.
