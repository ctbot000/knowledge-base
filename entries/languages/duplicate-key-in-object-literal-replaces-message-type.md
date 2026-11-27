---
title: A payload field named like a message's type key silently replaces the type in an object literal
tags: [javascript, json, protocols, debugging]
added: 2026-11-28
---

## Fact

A JavaScript object literal may repeat a key: the last value wins, with no error
and no warning at run time (only some linters flag it). In a message such as
`{ t: 'op', at: 1, t: clock }`, a field meant as "time" overwrites the type field
`t`, and `JSON.stringify` sends a message whose type is a number.

## Why it matters

Routers that dispatch on the type field drop such a message quietly (no case
matches, or a typeof check rejects it), so the sender sees nothing happen and
nothing is logged. It looks like a validation or timing bug on the receiving end.

## How to apply

- Keep envelope keys (type, id) out of every payload's vocabulary: name a time
  `at` or `ms` when the type key is `t`.
- Turn on `no-dupe-keys` (ESLint) or an equivalent check where messages are built
  as literals.
- When a message "does nothing", log what the router receives before suspecting
  the handler.
