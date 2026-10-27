---
title: node --test reruns only the failed tests with --test-rerun-failures, the built-in way to retry flaky tests
tags: [node, testing, flaky-tests, ci]
added: 2026-10-27
sources:
  - https://nodejs.org/api/cli.html#--test-rerun-failures
---

## Fact

`node:test` has no per-test retry count, but `node --test
--test-rerun-failures=<state.json>` records each test's result in that file.
Run the same command again with the same file and only the tests that have
not yet passed run; the others are reported as passed ("passed on attempt 0").
Verified on Node 26.

## Why it matters

Without it, retrying a flaky suite means rerunning everything or scraping
failing test names into `--test-name-pattern`, which breaks on names with
regex characters and on duplicated names. Hand-rolled retry wrappers or a
second test framework are unnecessary.

## How to apply

- Rerun the identical command with the same state file once if it exits
  non-zero; it passes if the failed tests now pass. Use one state file per
  process when a runner spawns several (shards, files).
- Tests are keyed by `file:line:col`. Tests created at one call site (a
  wrapper such as a sharding `test()`) get an occurrence suffix (`:(1)`,
  `:(2)`), so they are still told apart, as long as each run registers the
  same tests in the same order.
- `before` hooks run again on the rerun, so the browser or server setup
  repeats; only the tests are skipped.
- The rerun's `ℹ tests` / `ℹ pass` count the whole file, earlier passes
  included, so add up the totals from the last run only, not from both.
- Record which tests passed only on the rerun and print them, so flakiness
  stays visible instead of being hidden.
