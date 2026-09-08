---
title: Sweep the action space before tuning difficulty — "hard" and "impossible" look identical from inside the game
tags: [game-design, simulation, testing]
added: 2026-09-08
---

## Fact

When success depends on a continuous control input — an aim angle, a launch
power, a steering curve — you can measure how hard the game actually is by
brute-forcing that input from real positions and counting what scores. Two
numbers come out of it:

- the fraction of positions that have **any** winning input at all, and
- the fraction of the input space that wins, when one exists.

Both are cheap to get if the simulation can be replayed headlessly, and neither
is visible from playing.

## Why it matters

A physically faithful carom table with heavy cloth and dead cushions gave, under
a sweep of 3600 angles by 4 powers, **no scoring stroke at all in nine of twenty
positions**, and about 0.05% of strokes elsewhere. From the inside that reads as
a weak opponent and unfair aiming aids, and it invites tuning the search, the
guide lines, and the difficulty curve — none of which can reach a position with
no solution.

Livelier cushions, faster cloth and a slightly smaller table took it to twenty
of twenty solvable. The same unchanged search code went from 20% to 50% success.
The knob that mattered was in the physics; every knob reached for first was in
the agent.

## How to apply

- Sample finer than the success window you expect. If a sweep at 0.1° finds
  isolated hits, the window is near that width and a coarser sweep would have
  reported zero.
- Sweep from positions the game actually reaches — drive them forward with an
  existing agent between samples — not only from the opening state.
- Report solvable-position rate separately from win-rate. They fail differently:
  the first is a design fault, the second a tuning one.
- Near-zero density means change the world, not the search.
- Keep the sweep as a script and re-run it after any physics change; it is the
  only thing that distinguishes a hard game from a broken one.
