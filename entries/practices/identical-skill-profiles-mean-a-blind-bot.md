---
title: When every simulated skill level scores the same, the fault is the bot's perception
tags: [game-design, simulation, testing, balance]
added: 2026-09-11
---

## Fact

Balance runs across skill profiles are read for their spread. When the spread
collapses — perfect, expert, average and beginner all landing on the same
median run length and the same median score — the cause is almost never the
game. It is that the controller cannot see something, so every profile fails
the same way for the same reason and the injected error never gets to matter.

The usual blind spot is a perception filter written as "what is ahead of me".
An agent that selects hazards with `z > 0` drops the one it is currently
inside, and then acts on the *next* one: it starts a sidestep, or stands up out
of a crouch, while still overlapping the thing it just cleared.

## Why it matters

The reading is inverted. Identical medians with a perfect controller dying at
20 seconds says "this game is unfair and needs to be made easier", which is a
change to the wrong system — and one that will hold, because the bot will keep
dying at 20 seconds afterwards.

It is also distinct from an error model that is too weak to bite. There the
profiles collapse onto the *good* end and everything survives; here they
collapse onto the bad end and the perfect run dies too. The perfect run is the
discriminator: it has no injected error at all, so if it dies at the same rate
as a noisy one, nothing about the noise is reaching the outcome.

## How to apply

- Check the flawless profile before the numbers: a controller with zero error
  should approach the fair-play ceiling. If it does not, fix the controller.
- Make the agent's perception include what currently overlaps it, not only what
  lies ahead, and forbid state changes while that set is non-empty.
- Log what killed each run, not just when. Deaths clustering on one obstacle
  type, or on one internal state such as "mid-transition", names the blind spot
  directly.

Related: [[simulated-error-is-per-decision]], [[flawless-player-measures-survival]],
[[balance-knob-with-no-effect]].
