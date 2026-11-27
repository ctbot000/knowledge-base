---
title: A function's length and name are read-only, so using one as a namespace breaks on those two keys
tags: [javascript, functions, strict-mode]
added: 2026-11-27
sources:
  - https://tc39.es/ecma262/#sec-function-instances-length
---

## Fact

Every function has own `length` and `name` properties that are not writable.
`fn.length = 42` throws "Cannot assign to read only property 'length' of
function" in strict code, ES modules included, and does nothing at all in
sloppy code.

## Why it matters

A callable with properties attached (`c(name)` plus `c.length`, `c.all`, …) is
a common helper shape, and `length` and `name` are the natural keys for "how
long" and "what it is called". In a module the helper throws on first use; in
an old script it silently keeps the parameter count.

## How to apply

- Pick another key (`total`, `title`) for properties hung on a function.
- `Object.defineProperty(fn, 'length', { value })` works if it really must be
  `length`, since the property is configurable.
