---
title: A duplicate case label in a JavaScript switch is legal, and the later one never runs
tags: [javascript, debugging]
added: 2026-11-07
sources:
  - https://tc39.es/ecma262/#sec-runtime-semantics-caseblockevaluation
  - https://eslint.org/docs/latest/rules/no-duplicate-case
---

## Fact

JavaScript has no early error for two `case` clauses with the same value, in
strict mode or not. The first match wins, and the later clause is dead code. The
engine says nothing.

## Why it matters

The risk is in long `switch (name)` dispatch tables, for sounds, messages or
effects, that grow one clause at a time. A new `case 'whirl':` added for a new
feature, when one already sits three hundred lines up, parses and runs: calling
it does the old thing. Nothing fails, and only a person listening or looking
notices that the new behaviour never happens. A test that only checks the name
was played passes too.

## How to apply

- Turn on ESLint's `no-duplicate-case`, which is in its recommended set.
- Without a linter, grep for the label before adding a clause to a long switch.
