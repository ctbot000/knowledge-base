---
title: A plain object used as a whitelist lets "constructor" and "toString" through, with `in` or with a truthy lookup
tags: [javascript, validation, security]
added: 2026-11-25
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/in
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn
---

## Fact

`key in TABLE` and `TABLE[key]` both see the inherited members of
`Object.prototype`, so `'constructor'`, `'toString'`, `'valueOf'` and
`'__proto__'` all pass a check written as `key in TABLE` or `if (!TABLE[key])`.

## Why it matters

The check guards the one place where the key comes from outside: a message, a URL,
a saved file. A bad name passes, and the next line calls `Object` or reads a
function as if it were a record, which crashes far from the check or, worse, does
not. Tests with ordinary wrong names never catch it.

## How to apply

- `Object.hasOwn(TABLE, key)`, a `Map`, or `KEYS.includes(key)` over
  `Object.keys(TABLE)`.
- Put `'constructor'` in the list of wrong names a validation test tries.
