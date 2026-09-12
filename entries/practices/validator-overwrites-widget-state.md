---
title: A submit function that stores its own argument overwrites the widget state it was derived from
tags: [ui, state, frontend]
added: 2026-09-12
---

## Fact

A widget's live state and the value it submits are often the same information
in two representations — dial positions as indices into a symbol list, and the
symbols themselves. Writing the submitted value back into the widget's field
re-types it:

```js
export function submitCode(s, symbols) {
  s.dials = symbols.slice();     // the panel reads s.dials as indices
  ...
}
```

Nothing fails at the call. The widget was rendered before the submit and its DOM
is untouched, so a rejected attempt looks completely normal. The break appears
the next time the widget is *built from state* — a later reopen, a re-render, a
restored save — and then it renders from `SYMBOLS['anchor' % SYMBOLS.length]`,
which is `undefined` rather than an error.

## Why it matters

Cause and symptom are separated by an arbitrary interval and by a user action
the failing flow does not perform, so the bug never shows up in the interaction
that creates it. A test that calls submit and asserts on its return value
passes. So does a play-through that gets the answer right first time.

If the state is persisted, the corruption is persisted with it: the reload
restores a widget that cannot draw itself, and the control is dead for good.

## How to apply

- Give a field one writer. If the validator needs a record of the attempt, give
  it its own field rather than borrowing the widget's.
- Convert at the boundary instead of into storage: `submit(dials.map((i) =>
  SYMBOLS[i]))`, and leave `dials` holding indices.
- Test the reopen, not the call. After a rejected submission, rebuild the widget
  from state and assert it still renders — that is the assertion that fails.
- A field that gets persisted is a schema. Assert its element type in a test if
  more than one module writes it.
