---
title: An explicit damper between two inertias is stable on their reduced inertia, and a gear ratio shrinks it by the ratio squared
tags: [simulation, physics, numerics, game-design]
added: 2026-09-19
---

## Fact

Coupling two rotating bodies with a spring-damper and integrating explicitly is
the usual way to avoid writing a constraint solver. It is stable only while

```
c * dt / I_red < 2,      I_red = 1 / (1/I1 + 1/I2)
```

where `I_red` is the **reduced** inertia of the pair, not either body's own. A
binary search on `c` puts the threshold at 2.001 for every combination of `I1`,
`I2` and `dt` tried — it is a property of the scheme, not of the numbers.

A gear ratio `n` between the two bodies is what makes this bite, because the far
inertia referred to the near side is `I2 / n²`. With a 0.26 kg·m² crank, a
2.4 kg·m² axle, `c = 26` N·m·s/rad and `dt = 1/400` s, the same coupling is
comfortably stable in a 3.13:1 gear (`c·dt/I_red = 0.52`) and diverges within
ten steps in a 13.5:1 one (`5.19`).

## Why it matters

The symptom is not a NaN. It is a plausible-looking oscillation: torque
alternating at its clamp, contact forces flipping sign every step, a body
juddering. That reads as a friction, contact or controller problem, and it
appears only in the configurations with the largest ratio — first gear, a
winch's low range, a reduction drive — so it survives every test taken in the
others.

Raising the substep rate helps, and halving `dt` only halves the number, so the
fix looks like it "nearly worked" and invites more of it.

## How to apply

- Compute `c * dt / I_red` at the **worst** ratio in the system and keep it
  under about 1. That is a two-line assertion worth having permanently.
- Where the ratio is large, drop the compliance: treat the coupling as either
  locked — one rigid body, the small inertia added to the large one — or
  slipping at a bounded torque, and choose per step from the torque the rigid
  solution would demand. That is unconditionally stable and needs no solver.
- Related: [[friction-must-scale-with-normal-impulse]].
