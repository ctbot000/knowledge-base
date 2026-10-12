---
title: A failing node:assert equality on objects holding big arrays can take gigabytes to build its message
tags: [node, testing, assert, memory]
added: 2026-10-12
sources:
  - https://nodejs.org/api/assert.html
  - https://github.com/nodejs/node/issues/61346
  - https://github.com/nodejs/node/pull/61347
---

## Fact

When `assert.strictEqual` (`equal` from `node:assert/strict`) or
`deepStrictEqual` fails on two objects, Node diffs the full `util.inspect` text
of both (every array element on its own line) with a Myers diff that keeps a
copy of its whole work array per step of edit distance, so memory grows with
lines × differences: roughly the square of what the objects hold. On Node 26, two objects of eight `Float32Array`s each took 0.3 GB
at 1,000 elements per array, 4.3 GB at 4,000 and 66 GB at 16,000, for a message
of under a megabyte. `--max-old-space-size` does not cap it. Known upstream
(nodejs/node#61346); a fix that truncates and chunks the diff is proposed.

## Why it matters

One assertion that starts failing after a refactor stops the run instead of
reporting: the test hangs while the process eats the machine's memory until it
is killed (`node --test` then reports only the file as failed, by `SIGKILL`,
with no subtest output). Scene-graph nodes such as three.js `Object3D`s are the
usual trigger: through `parent` and `children` either one reaches every
geometry's typed arrays, so comparing two small groups in a model is enough.

## How to apply

- Compare object identity with a boolean: `assert.ok(a === b, 'in the hand')`,
  never `assert.equal(a, b)` on graph nodes, buffers or anything holding them.
- Deep-compare plain data only: map big objects to the few fields that matter
  (`a.children.length`, a name, a checksum) and compare those.
- When a run dies with no output, re-run the suspect test alone under
  `perl -e 'alarm 60; exec @ARGV' node --test …` and watch its memory.
