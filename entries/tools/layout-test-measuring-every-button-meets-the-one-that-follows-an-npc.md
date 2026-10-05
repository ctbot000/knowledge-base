---
title: A layout test that measures every HUD button flakes when one of them follows a wandering character
tags: [testing, layout, ci, game, flaky-tests]
added: 2026-10-05
---

## Fact

A prompt that floats over a simulated character (a "Ride" or "Talk" button over
the nearest animal, a name tag) is placed by the simulation, not by the layout.
A test that loops over every button in the HUD (`#hud button`) to check that
nothing overlaps includes it whenever a character wanders within reach of the
player, which depends on the seed and on how long the test has run.

## Why it matters

The check fails only on those runs, with the floating element's name as the only
clue (`['ride']` lying under a chat line), so it passes locally and in most CI
runs and looks like a layout regression. Standing still for forty seconds on a
generated island, a wandering animal came within reach on about one island in
twenty-five (found by running the simulation offline, no browser).

## How to apply

- Keep floating elements out of static layout checks: inject
  `#ride { display: none !important }` after setup. The app keeps running its own
  code on the element (removing it would throw), and the measurements see a
  zero-size box.
- Reproduce before trusting the fix: put the player beside a parked entity so the
  prompt is up for the whole test, and the unfixed test fails at once with the CI
  message; the fixed one passes.
- Give the floating element its own test with its entity forced into place, if
  its position matters.
