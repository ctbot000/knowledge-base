---
title: Where power comes from the player's motion, an interception AI that arrives early and stops is useless
tags: [game-design, ai, simulation]
added: 2026-09-08
---

## Fact

In any game where the return is a reflection off the player's body — volleyball,
pinball flippers, a bat, a deflector shield — the outgoing energy is the incoming
energy plus whatever the player's own velocity adds. A stationary body returns
strictly less than it received.

So the obvious interception AI is wrong in a way that looks right: predict the
landing point, walk there, wait. It arrives perfectly positioned and stationary,
and its return is a pure damped reflection that cannot clear the obstacle. The
symptom is not a miss — the AI touches the ball every time — it is a return that
keeps falling short, which then reads as a rules failure downstream (a
touch-limit fault, a self-inflicted point).

Tuning the standing offset does not fix it: the whole trade sits between "too
close, pops it straight up" and "too far, misses entirely", and both ends are
worse than the middle.

## Why it matters

Every symptom points away from the cause. Contacts are being made, position
prediction is provably correct, and the fault that ends the rally is three
touches later. The natural response is to raise restitution or lower the barrier
— changing the physics to compensate for a movement policy, which then makes the
*human* game floaty in exchange.

## How to apply

- Give the AI two phases: hold a loading position further back while there is
  time, then drive through the contact point so it is still moving on impact.
  Trigger the switch on predicted time-to-contact, not on distance.
- Measure the fault it causes, not the contact rate. Contacts-per-rally looks
  healthy throughout; the share of points lost to self-inflicted faults is what
  moves.
- The same shape appears wherever an agent's effectiveness depends on its state
  at the moment of an event rather than on being in the right place.

Related: [[tracking-target-vs-slew-rate]], [[simulated-error-is-per-decision]].
