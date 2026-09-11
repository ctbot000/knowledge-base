---
title: A moving hazard must commit its path before it enters the player's reaction window
tags: [game-design, balance, simulation]
added: 2026-09-11
---

## Fact

A hazard that keeps choosing where to be while it closes on the player is not
difficult, it is unavoidable. Once it is within reaction distance, any further
movement of its own arrives with less warning than a human can answer, so the
outcome is decided by where it happened to drift rather than by play.

The fix is not slower movement — halving the speed halves the warning needed
and leaves the same hole. It is to split the approach: the hazard may move
freely while it is far away, then lock onto a final track and hold it for the
whole of the player's reaction window.

## Why it matters

These deaths are rare enough to look like ordinary difficulty and are almost
invisible in aggregate statistics — a few percent of runs, scattered. They show
up as a flawless controller dying occasionally with no explanation, which reads
as noise rather than as a rule violation.

They are also the deaths players remember, because the correct response was
made and punished anyway.

## How to apply

- Give the hazard two phases with an explicit handover distance: free movement
  beyond it, committed within it. Ease into the committed track rather than
  snapping, or the commit itself is a teleport.
- Size the handover from the worst case — maximum approach speed times the
  reaction budget you intend — not from how it looks at the speed you happen to
  be testing.
- Assert it: over a long automated run with a flawless controller, no death may
  occur where the hazard moved laterally inside the window. A perfect player
  dying at all is the signal to go looking.
