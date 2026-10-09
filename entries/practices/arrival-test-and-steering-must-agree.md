---
title: An agent whose "arrived" test is stricter than its steering goal parks short of the goal for good
tags: [simulation, ai, game-design]
added: 2026-10-09
---

## Fact

When the check that says "there, act now" asks for more than the goal the
movement code steers toward (a height as well as a horizontal distance, say),
the agent stops inside its steering radius, believes it has arrived, and never
satisfies the check. A stuck detector that only measures horizontal progress
never fires either, because the agent is not trying to move.

## Why it matters

Nothing errors and nothing looks stuck: the agent stands still, steering
reports "reached", and the task waits on whatever fallback timeout exists. A
per-step fallback ("give up after 15 s, do one step") turns into a 15 s stall
per step. The same blind spot hides an agent rising in place under a ceiling:
it is within horizontal reach, so it is not "moving", so it is never "stuck".

## How to apply

- Derive both from one predicate: whatever makes "near" false must also make
  the steering goal ask for that movement (e.g. `flyTo: up > 2 || tooLow`).
- Measure progress on every axis the goal asks for; count "wanting to rise"
  as moving, and when stuck with no horizontal error, step sideways in a
  direction that changes over time.
- Reset a give-up timer only on actually arriving, not on each step done via
  the fallback, so one give-up covers the whole stretch away.
- Reproduce under load (a background-priority run) — slow ticks expose it.
