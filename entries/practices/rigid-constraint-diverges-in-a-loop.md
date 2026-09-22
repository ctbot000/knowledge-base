---
title: A rigid constraint solved with a Baumgarte bias diverges in a network with loops, and more iterations makes it worse
tags: [simulation, physics, numerics]
added: 2026-09-22
---

## Fact

The usual rigid distance constraint removes the relative velocity along its axis
and corrects drift with a Baumgarte bias, with no compliance at all:

```js
this.gamma = 0;                       // infinitely stiff
this.bias  = 0.2 * invDt * error;
```

It is stable alone, and stable in a chain. It diverges in a **network with
loops** — a cloth grid, a truss, anything where a constraint's two endpoints are
also connected by another path. Gauss-Seidel plus warm starting amplifies the
residual instead of shrinking it: in a 14x10 grid the constraint force settles at
roughly a thousand times the mesh's own weight.

Giving the same joint a finite stiffness fixes it. Expressed as an implicit soft
constraint at 40 Hz with a damping ratio near 1, the force stays under a few
hundred times a node's weight and the mesh comes to rest — while a single rod
still holds its length to a fraction of a percent.

## Why it matters

The distinguishing symptom is that **raising the iteration count makes it
worse**, not better. Everywhere else in a solver more iterations means better
convergence, so the instinct is to add them, and the numbers get larger. That
sends attention to contacts, masses or the timestep rather than to the joint.

It also hides completely in the configurations most joints are tested in — a
pendulum, a rope, a bridge — because a tree has no loops.

## How to apply

- Do not model "rigid" as zero compliance. Model it as a very stiff implicit
  spring, and cap the frequency at a fraction of the step rate:
  `f = min(40, 1 / (3 * dt))`.
- Test a joint type in a loopy network, not only in a chain, and watch total
  constraint force over time rather than positions.
- Treat "adding iterations made it worse" as a divergence signature, and look
  at the constraint formulation rather than the solver.

Related: [[damper-stability-follows-reduced-inertia]].
