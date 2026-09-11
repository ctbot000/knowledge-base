---
title: A simulated player that waits on its target absorbs everything that arrives there first
tags: [game-design, simulation, testing, balance]
added: 2026-09-11
---

## Fact

In any game where the agent collects, triggers or takes damage from whatever it
occupies — a catcher on a line, a pickup radius, a hitbox moving through a
bullet field — *when* it arrives somewhere is part of the policy, not an
implementation detail.

The obvious controller picks a target and steers at it immediately, then sits
there until the target arrives. That is a much worse policy than it looks:
everything else that reaches the same spot during the wait is collected too.
A human plays the other way round, hanging back in a gap and stepping in at the
last moment, and the difference is not small. In a bead-catching game where
anything the needle passes under is threaded, switching the bot from "go now"
to "arrive just in time":

| | camping | just-in-time |
|---|---|---|
| wrong items collected per run | 19 | 2 |
| clean objectives completed | 7.7 | 19.4 |
| score separation, flawless vs good | 1.32x | 2.06x |

The commit test is one line: move when `timeToArrival <= travelTime + reaction`,
and wait in the safest reachable spot until then.

## Why it matters

The overhead gets charged to the game. A flawless controller collecting one
penalty per objective reads as "the level geometry leaves no room to avoid
them", so the fix goes into the world — wider lanes, slower hazards, a gentler
curve — where it does nothing, because the controller will keep camping
afterwards. Two structural changes can be made, verified as ineffective, and
kept, before anyone suspects the bot.

It also flattens exactly the measurement the sweep exists for. A cost every
profile pays equally compresses the skill spread, so a design that does separate
skill is reported as one that does not, and the compounding bonuses built to
reward clean play never fire in the simulation.

The tell is a controller with **no injected error at all** still producing the
game's own error type at a steady rate. Injected error cannot explain it, so the
policy has to.

## How to apply

- Separate approach from arrival in the controller: choose the target early,
  commit to the position late.
- Give "wait somewhere safe" a real implementation. Parking spots must include
  the gaps *between* the places things arrive — a bot that only ever considers
  lane centres is standing in the traffic it is trying to avoid.
- Before trusting a sweep, check the flawless profile's rate of avoidable
  mistakes. Anything well above zero is a controller bug until proven otherwise.
- Re-run the world change you already made after fixing the bot; it may have
  been unnecessary.

Related: [[identical-skill-profiles-mean-a-blind-bot]],
[[flawless-player-measures-survival]], [[balance-knob-with-no-effect]],
[[simulated-error-is-per-decision]].
