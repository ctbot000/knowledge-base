---
title: A no-guess puzzle board is found by rejection sampling against a solver that only makes the player's deductions
tags: [algorithms, puzzles, game-design, generation]
added: 2026-08-31
---

## Fact

There is no need to *construct* a logically solvable puzzle. Generate a random
board, replay it with a solver restricted to the inferences a player can
actually make, and keep the board only if that reasoning reaches every square.
Otherwise throw it away and draw again.

The solver is the specification of fairness, so it must be deliberately weak:
give it only the rules you expect a person to use, never a search over all
consistent configurations. For a Minesweeper-shaped puzzle that is three rules —
a clue whose mines are all marked frees its remaining neighbours; a clue with as
many unknowns as missing mines marks them all; and one clue's unknowns nested
inside another's settles the difference. A global "n mines remain" pass closes
the endgame.

## Why it matters

Rejection sampling is the whole algorithm, and on small boards it is far cheaper
than it sounds — thousands of candidates per second — so a board can be drawn at
the moment of the first click, once the opening square is known and can be
guaranteed empty. Trying to build guaranteed-solvable boards directly is much
harder and tends to produce a recognisable house style of puzzle.

The cost is not flat, though: acceptance collapses as density rises. Measured on
small square grids, roughly a quarter of the squares being mines is accepted
almost always, a third is accepted about half the time, and beyond that most
candidates need a guess. Difficulty therefore has a ceiling set by the sampler,
not by taste.

## How to apply

- Budget attempts rather than looping forever, and keep the best candidate seen
  so the game still starts if none is clean. Tell the player when it is not.
- Measure the acceptance rate per difficulty before shipping a ladder; set the
  hardest level where acceptance is still near 1, not where the puzzle is merely
  possible.
- Full clearance is its own proof: a solver that opens exactly the safe squares
  cannot have marked a safe one by mistake, so soundness needs no separate test.
