---
title: A wrapper around node:test's test() makes every test report the wrapper's line as its location
tags: [node, testing]
added: 2026-10-19
---

## Fact

node:test records a test's file, line and column from the direct caller of
`test()`. Call it through a helper — `const test = (...a) => keep() && real(...a)`,
to shard, filter or tag tests — and every test is reported at the helper's
line: the failure summary's `test at file.js:50:57` is the same for all of them.

## Why it matters

The location is how a reader jumps from a failure to its test. Through a
wrapper it points at plumbing, and an agent or editor following it reads the
wrong code. The test name and the stack trace inside the test body stay right.

## How to apply

- Keep the real `test` whenever the wrapper has nothing to do:
  `const test = sharded ? wrapper : realTest`, so plain runs keep exact lines.
- Where the wrapper is needed, print another way to find a failed test, such as
  a ready-to-run `--test-name-pattern` command with the name escaped as a regex.
- The location comes from the call stack; there is no option to pass one in.
