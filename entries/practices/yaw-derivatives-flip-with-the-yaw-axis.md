---
title: Published yawing-moment derivatives assume the yaw axis points down, so a Y-up engine frame needs every one of them negated
tags: [simulation, physics, 3d]
added: 2026-09-19
---

## Fact

Flight-dynamics derivatives are quoted in the NED body frame: x out the nose,
y out the right wing, **z down**. A positive yawing moment there swings the nose
right, so weathercock stability is written `Cn_beta > 0`.

Game and graphics engines put the vertical axis up. In that frame a positive
moment about the vertical swings the nose *left*, so the same physical stability
is `Cn_beta < 0`. Copying the published sign inverts it, and the fin now pushes
the nose further out of the wind instead of back into it.

Three rules cover the whole conversion:

- **Yawing moments** (`Cn_beta`, `Cn_dr`, `Cn_da`, `Cn_p`) flip sign.
- **Rolling moments, pitching moments and side force** do not: their axes are
  unchanged.
- **Damping terms that pair a moment with its own rate** (`Cn_r`) keep their
  sign, because the coefficient and the rate both flip and the product does not.

That last one is the trap: a mixed table where two of the three rules have been
applied looks self-consistent.

## Why it matters

The aircraft still flies. It sits on the ground correctly, accelerates, rotates
and climbs away, because nothing in the longitudinal axis is wrong. The
divergence starts at a fraction of a degree of sideslip and doubles every few
seconds, so the failure appears a minute into the flight as a slow, smooth
departure that reads as a control-mixing bug, a gust, or bad damping tuning.

## How to apply

- Write the frame down where the derivatives live, and state in a comment that
  the yaw-axis sign is inverted relative to the source. Future readers will
  otherwise "fix" it back.
- Test it directly rather than by flying: kick the yaw rate, hold the controls
  fixed, and assert that `|beta|` decays. A stable airframe halves it in seconds;
  an unstable one is unmistakable in twenty.
- The same reasoning applies to any ported table of signed coefficients —
  torque curves, magnetometer axes, joint limits. Only the terms whose axis
  actually flipped change sign.
