---
title: node --test started from inside a node:test run inherits NODE_TEST_CONTEXT and exits 0 even when its tests fail
tags: [node, testing, child-process]
added: 2026-10-17
---

## Fact

The test runner sets `NODE_TEST_CONTEXT` in the environment of each test
file's process. A `node --test` spawned from inside a test (or from code a
test exercises) inherits it, takes itself for the runner's child, reports its
results to a parent that is not listening, and exits 0 whether its tests pass
or fail. Its printed output no longer says `✖ … fail N` either.

## Why it matters

Code that runs a project's tests as a gate — a CI helper, a bot that checks a
change before opening a pull request — passes everything while under test, so
its own tests prove nothing about the gate, and a test asserting "the failing
suite is caught" fails in a confusing way (or passes for the wrong reason).
Outside a test run the same code behaves correctly, which hides the cause.

## How to apply

Drop the variable from the child's environment whenever spawning the runner:

```js
const { NODE_TEST_CONTEXT, ...env } = process.env;
execFile(process.execPath, ['--test', file], { env });
```

Do it in the production code, not only in the test, so the gate is the same
code in both places.
