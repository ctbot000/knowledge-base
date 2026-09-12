---
title: A rate-limited agent must score where it will be on arrival, not the candidate position itself
tags: [game-design, control, simulation, ai]
added: 2026-09-12
---

## Fact

An avoidance controller usually evaluates candidate positions — lanes, slots,
gaps — and moves toward the cheapest. If the cost is evaluated *at the
candidate*, the agent keeps choosing gaps it cannot physically reach, because
nothing in the cost knows that moving there takes time.

Evaluating the same cost at the position the agent will actually occupy when the
threat arrives fixes it without a separate reachability rule:

```js
const t = clamp(threat.timeToContact, 0.15, 2.5);
const reached = Math.min(Math.abs(x - pos), slewRate * t);
const at = pos + Math.sign(x - pos) * reached;
cost += penalty(Math.abs(at - threat.centre));
```

Far-off threats saturate at the candidate, so the behaviour is unchanged where
there is time; near ones collapse toward the current position, which is the
truth.

## Why it matters

The failure is not that the agent freezes — it commits to a gap, travels
partway, and is hit in between, which looks like a tuning problem in the cost
weights. Turning up the avoidance penalty makes it worse, because the
unreachable gap is exactly the one the penalty is pushing hardest toward.

Where such a controller is the measuring instrument for balance, the extra
collisions are charged to the level design, and the difficulty gets tuned around
a defect in the observer.

## How to apply

- Bound the urgency divisor. A threat already alongside has a time to contact of
  zero, and `1/ttc` then swamps every other term, leaving the cost landscape
  flat and the choice effectively random.
- Aim for the middle of a gap, not its edge: add a soft penalty below a
  clearance that a lane-width gap can actually offer. Without it the agent
  threads at the contact threshold and one step of drift is a collision.
- Decide to slow down on a fixed time horizon, not on the time it takes to
  steer. Shedding speed takes far longer than changing lane, so deciding once
  the gap has closed is deciding too late.
