---
title: A rollback check that waits for an assumed empty value fails as an intermittent timeout on random fixtures
tags: [testing, flaky-tests, debugging]
added: 2026-10-01
---

## Fact

A test that verifies a refused or undone change by waiting for the target to
become "empty" (`0`, `null`, air, no row) is asserting a starting state it never
checked. With generated fixtures (random worlds, seeded data, live accounts) the
target is sometimes not empty to begin with; the rollback correctly restores
what was there, and the wait can never succeed.

## Why it matters

The failure arrives as a polling timeout, usually on the slowest runner, so it
reads as CI slowness and gets "fixed" with a re-run or a longer timeout. The
code under test is right; the expectation is wrong on a fraction of fixtures,
which is why it passes locally and on most CI runs.

## How to apply

- Capture the value before the action and wait for a return to that value:
  `const was = read(cell); act(); await until(() => read(cell) === was)`.
- When the test really needs an empty start, make it empty (or pick a target
  that is) instead of assuming it.
- When a "slow CI" timeout repeats on the same step, log the value being waited
  on before raising the limit: a value that settled on something else is a
  wrong expectation, not a slow machine.
