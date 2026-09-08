---
title: A boundary clamp applied during integration must run again after collision resolution
tags: [game-design, collision, simulation]
added: 2026-09-08
---

## Fact

The usual step order is integrate, clamp to the world bounds, then resolve
collisions with other bodies. Positional collision resolution teleports the
moving object out along the contact normal — and that displacement does not
know about the world bounds the clamp just enforced.

So a body pressed against a wall pushes whatever it collides with *through* that
wall. The object ends the step embedded in the boundary, past a clamp that ran
correctly a few lines earlier.

It only happens within one object-radius of an edge, and only while something is
holding position there, so it survives ordinary play and ordinary tests.

## Why it matters

The clamp is present, is correct, and is the first thing read when the bug is
reported — which makes the boundary code look exonerated. Attention then goes to
the collision resolver, which is also correct. The defect is in neither: it is in
the order.

Visually it is a sliver of an object outside the play area, easy to dismiss as a
rendering or camera artifact rather than a state error, so it tends to be found
by an invariant rather than by looking.

## How to apply

- Re-apply the clamp after every step that can move the body: resolve collisions,
  *then* clamp again. It is idempotent, so running it twice costs nothing.
- Reflect velocity on the second pass only when the body is still moving into the
  boundary, or a rebound gets applied twice.
- Assert the invariant every step over a long automated run rather than trusting
  the clamp: `assert(r <= x <= W - r)` finds this in seconds and pins it against
  later reordering.
