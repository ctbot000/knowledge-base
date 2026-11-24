---
title: A fight whose enemies lose at most one hit point per opening lasts as long as its openings, however strong the weapon
tags: [game-design, combat, balance]
added: 2026-11-25
---

## Fact

When damage is multiplied by weapon power, a late weapon divides every fight's
length by its multiplier, and extra enemy health only tunes one point of that
curve. If instead an enemy guards itself, can be hurt only in short openings earned
by a right action (a late dodge, a counter, a trick of its own), and an opening takes
one unit of health at most before the guard is back up, the number of openings sets
the length. Weapon power is left a small, bounded effect: how much of an opening a
unit takes.

## Why it matters

Scaling enemy health to the equipped weapon is the usual fix and it makes upgrades
feel pointless or punishes friends with different gear. Gating by openings keeps the
upgrade visible (an opening is easier to use up) while every fight still asks for
the skill it was built around, for one player or several with mixed gear.

## How to apply

- Cap the benefit explicitly: for example three hits of the weakest weapon per
  opening and two of the strongest.
- Make mashing no way in: a hit on the guard costs a moment (a recoil), and a counter
  counts only if the button was not pressed just before.
- Let some openings come by themselves (after a long attack), so a player who cannot
  yet dodge still progresses.
- Test the property directly: thousands of hits with the strongest weapon on a raised
  guard take nothing, and one opening never takes two units.
