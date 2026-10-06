---
title: A ground probe that marks a falling body grounded before contact hides the landing from anything keyed on the airborne flag
tags: [game-design, collision, simulation]
added: 2026-10-06
updated: 2026-10-06
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
height-dependent share of landings; being intermittent, it reads as an audio or
effects glitch. A bounce pad keyed on the airborne-to-grounded transition loses
about half its bounces, and with jump held the standing-jump branch replaces
the speed carried down, so a "higher each bounce" mechanic resets at random.

## How to apply

- Key impact logic on the contact's own normal speed (faster than one substep
  of gravity gives a resting body), not on the grounded flag left by the
  previous substep.
- In the jump-from-ground path, check whether the body is still moving down:
  inside the probe band it is landing, and that fall speed belongs to the
  impact.
- Fix the consumers too. A caller that also wants the flag false at the start
  of its frame (`if (landed && !wasGrounded)`) re-hides every landing whose
  early catch fell on a frame's last substep: still about one in five at 60 fps
  with two substeps a frame, after the physics reports them all.
- Test by dropping from a sweep of fractional heights and counting reported
  landings; every drop must report one, through the frame loop as well.
