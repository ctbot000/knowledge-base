---
title: A relative-error check needs a denominator that cannot vanish
tags: [testing, numerics, simulation]
added: 2026-09-19
---

## Fact

Two habits turn a correct result into a failing test.

**Dividing by one component of a vector.** Comparing a computed force field
against a reference with `abs(ax - ref) / abs(ref)` blows up wherever that
component passes through zero. In any symmetric configuration many of them do:
a particle at the centre of a cloud has near-zero net force in every axis while
its neighbours have large ones. The reported relative error was 74% for an
absolute error around 1e-9.

**Comparing against an expected value of zero.** `close(actual, 0, rtol)` has no
scale to multiply, so every relative tolerance collapses onto whatever absolute
floor the helper happens to use. A y-coordinate 2.6e-6 from the origin after a
full orbit of radius 0.5 is an excellent result and fails a 0.2% check.

## Why it matters

Both produce failures on correct code, which is expensive in a different way
from missing a bug: the natural response is to loosen the tolerance until it
passes, and a tolerance loosened to accommodate a divide-by-zero is no longer
testing anything.

## How to apply

- Normalise by the magnitude of the whole vector, not a component:
  `hypot(dx, dy, dz) / hypot(rx, ry, rz)`.
- Compare a distance against a scale the problem provides — "it returned within
  1e-3 of an orbit radius", not "its y is near zero".
- Summarise a field with a median and a high percentile rather than a maximum.
  One near-cancelling sample should not decide the verdict.
- Where a quantity genuinely has no natural scale, say so and use an explicit
  absolute tolerance instead of pretending a relative one applies.
