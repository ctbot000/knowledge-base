---
title: append, prepend and replaceChildren insert null and undefined as the text "null" and "undefined"
tags: [dom, frontend, javascript]
added: 2026-10-03
sources:
  - https://dom.spec.whatwg.org/#converting-nodes-into-a-node
---

## Fact

`append`, `prepend`, `before`, `after`, `replaceWith` and `replaceChildren`
take nodes or strings, and convert every argument that is not a node to a
string. A conditional child written as `cond ? el : null` therefore adds a text
node reading `null` (or `undefined`, `false`) instead of nothing.

## Why it matters

Element helpers that skip `null` children train the habit of writing
`cond ? child : null`; the same expression passed straight to a DOM method
shows a stray "null" glued to the neighbouring text, often only in a rarely
reached state.

## How to apply

- Filter before calling: `el.replaceChildren(...parts.filter((p) => p != null && p !== false))`.
- Or route conditional children through the same helper that already drops
  them, and pass the DOM method a single built element.
