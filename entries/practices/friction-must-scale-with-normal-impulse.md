---
title: Scaling tangential velocity by a fixed factor per contact bleeds a rolling body to a stop
tags: [simulation, physics, game-design]
added: 2026-09-10
---

## Fact

The obvious way to add friction to an impulse-based collision resolver is to
shrink the tangential part of the relative velocity by a constant:

```js
rv.t *= (1 - mu);
```

It is wrong for resting and rolling contact, because a body lying on a surface
is *re-resolved every substep*. At a 240 Hz step, `mu = 0.06` is not a 6% loss;
it is 6% two hundred and forty times a second. A ball rolls down a 25° ramp at
a crawl, and lowering `mu` only postpones the stall.

Coulomb friction has no such term. The tangential impulse is bounded by the
normal one, and a resting contact carries only the substep's worth of gravity:

```js
const jn = -(1 + e) * vn;            // normal impulse
const jt = Math.min(tangentSpeed, mu * jn);
```

So the same coefficient that grips hard on a fast impact costs a rolling body
almost nothing.

## Why it matters

The symptom is behavioural, not numerical: nothing is NaN, energy is not
diverging, and every collision is individually plausible. Bodies simply refuse
to travel along shallow surfaces, which reads as bad level geometry — a ramp
that is "not steep enough" — and gets fixed by tilting the world instead of the
model.

It also scales with the timestep, so raising the substep rate to fix a tunnelling
problem makes the friction worse, and the two changes look unrelated.

## How to apply

- Cap the tangential impulse by the normal impulse; never scale the tangential
  velocity by a bare coefficient.
- Put deliberate, small energy loss somewhere frame-rate independent instead —
  a drag term applied per unit time, `v *= 1 - k * dt`.
- Test it on the shallowest slope in the world, from rest. A body that creeps
  where it should roll is this bug, not the slope.
