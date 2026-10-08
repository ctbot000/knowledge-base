---
title: every() and the other array callbacks skip the holes of new Array(n), so a fresh sparse array passes every test
tags: [javascript, arrays]
added: 2026-10-08
sources:
  - https://tc39.es/ecma262/#sec-array.prototype.every
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays
---

## Fact

`new Array(n)` makes `n` holes, not `n` undefineds, and `every`, `some`,
`forEach`, `filter`, `map` and `reduce` never call their callback for a hole.
So `new Array(3).every((x) => x !== undefined)` is `true`, and `some` on it is
`false`. `includes`, `indexOf`'s cousin `findIndex`, `find`, spreading and
`for…of` do visit holes, as `undefined`.

## Why it matters

The natural way to collect numbered pieces as they arrive is to allocate
`new Array(total)` and fill slots. A "have all pieces arrived?" check written
with `every(p => p !== undefined)` then reports a buffer with one piece in it
as complete, and code that should discard or wait on a partial transfer treats
it as whole. Nothing throws; the test just answers wrong.

## How to apply

- Ask about missing slots with `parts.includes(undefined)`, which treats holes
  as `undefined`, or keep an explicit count of filled slots.
- Or allocate with `Array.from({ length: n })` / `new Array(n).fill(undefined)`
  when callbacks must see every index.
- In tests, cover the partly-filled case: a buffer with only slot 0 set.
