---
title: A test that assumes a random fixture's starting value fails as an intermittent timeout
tags: [testing, flaky-tests, debugging]
added: 2026-10-01
updated: 2026-10-03
---

## Fact

Two common test steps quietly assume what a generated fixture (random world,
seeded data, live account) holds before the test acts:

- waiting for a refused or undone change to leave the target "empty" (`0`,
  `null`, air, no row), when the target was not empty to begin with, so the
  correct rollback restores something else;
- provoking a change by setting a fixed value (`hat = 'crown'`), when the
  fixture sometimes holds that value already, so nothing changes and no event
  fires.

Either way the code under test is right and the wait can never succeed.

## Why it matters

The failure arrives as a polling timeout, usually on the slowest runner, so it
reads as CI slowness and gets "fixed" with a re-run or a longer timeout. It
hits only the fraction of fixtures that start in the assumed state, which is
why it passes locally and on most runs.

## How to apply

- Rollback: capture the value before the action and wait for a return to it:
  `const was = read(cell); act(); await until(() => read(cell) === was)`.
- Change: derive a value that differs from the current one, and assert on the
  value you derived: `const next = cur === 'crown' ? 'cap' : 'crown'`.
- When the test really needs a particular start, set it up instead of
  assuming it.
- When a timeout repeats on the same step, log the value being waited on (and
  the starting value) before raising the limit.
