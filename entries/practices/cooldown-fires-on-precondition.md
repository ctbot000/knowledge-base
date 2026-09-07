---
title: A cooldown that elapses while its precondition is false fires the instant the precondition becomes true
tags: [simulation, game-design, timers]
added: 2026-09-07
---

## Fact

A decision timer of the usual shape — `nextDecision = now + interval`, checked
only while some condition holds — keeps elapsing whether or not that condition
is true. By the time the condition arrives, the deadline is long past, so the
first check passes immediately:

```js
// Consulted only when this agent holds the ball, but ticking the whole time.
if (hasBall(p) && now >= p.nextDecision) decide(p);
```

The agent therefore acts on the first tick of acquiring the thing, every time.
There is no settling period, and the interval that was supposed to pace the
behaviour paces nothing.

## Why it matters

The symptom appears far from the timer. In a ball game, every player passed on
the frame they received, so possession sat near 1% and the ball was loose 99% of
the time — which reads as a physics, capture-radius or pass-weighting problem,
and all three are innocent. The same shape gives an ability that fires the
moment it is off cooldown, or a retry that fires the moment a queue becomes
non-empty regardless of the backoff that was meant to space attempts out.

It survives review because the arithmetic is correct: the deadline really has
expired. What is wrong is that it expired while the agent had nothing to decide.

## How to apply

- Arm the deadline when the **precondition becomes true**, not only when the
  action fires: on acquisition, set `nextDecision = now + settle`.
- A minimum-hold invariant is cheap to assert and pins it: measure the mean time
  between acquiring and releasing, and fail if it is near zero.
- The general rule: a timer must be reset at every edge that makes it relevant,
  not only at the edge that consumes it.

Related: [[simulated-error-is-per-decision]], [[sim-deadlines-in-sim-time]].
