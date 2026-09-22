---
title: A removal puzzle is dealt by taking a finished board apart, and the order that does it is the solution
tags: [procedural-generation, puzzles, game-design]
added: 2026-09-22
---

## Fact

Where every move removes pieces — mahjong solitaire, pair-matching boards,
peg-style clears — do not place pieces and then test whether the board can be
cleared. Run the game backwards:

1. Fill every slot with an unknown piece.
2. Find the slots that are *legal to take right now*, pick as many as a move
   consumes, and assign them a matching set.
3. Remove them and repeat until the board is empty.

Replaying those removals forward is a legal game, so the arrangement they
describe is solvable by construction. The generation order is not a by-product:
it is a certificate, worth returning with the deal and replaying in the test
suite move by move.

The one failure mode is the sampler stranding itself — a state with pieces left
but fewer legal slots than a move needs, such as two tiles where one sits on the
other. It is not a bug in the layout, so budget attempts and redraw with a fresh
stream rather than trying to prove it cannot happen.

## Why it matters

Generate-then-verify needs a solver, and a solver over a board with tens of
thousands of orderings is the expensive part of the program. Unbuilding needs
only the legality test the game already has, runs in milliseconds, and cannot
return an unsolvable board at all.

## How to apply

- Assign pieces at removal time, never beforehand; that is what keeps every step
  legal.
- Keep the certificate and assert it: replay it through the real move validator
  and require the board to reach empty.
- Reuse the same routine for an in-game reshuffle, over the slots and pieces
  still standing, so the rest of the game stays solvable too.
- Solvable is not the same as worth playing — see
  [[solvable-is-not-the-same-as-worth-solving]] — so also measure how often a
  player taking a *random* legal move clears it. Near 100% means the board is
  not a puzzle. [[no-guess-puzzle-generation]] is the counterpart for puzzles
  where the question is deduction rather than ordering.
