---
title: One key press runs two steps when a bubbling handler reads state an inner handler just changed
tags: [dom, events, keyboard, frontend]
added: 2026-08-27
updated: 2026-09-06
---

## Fact

Event dispatch is synchronous, and a handler that mutates application state
mutates it *before* the event reaches the remaining handlers on the propagation
path. A document-level handler written as "if the answer is already submitted,
advance to the next step" therefore fires on the very key press that submitted
the answer — the inner handler flipped the flag microseconds earlier in the same
dispatch.

The result is a single key press performing two steps: submit and advance, open
and close, add and confirm. The second step has two possible sources, and they
take opposite fixes: another *listener* on the propagation path, or the
browser's own *default action* when a handler acts on Enter or Space while a
`<button>` has focus — the handler runs during propagation, then the default
action fires that button's `click`. Moving focus in the inner handler invites
the second kind, and a single delegated handler is no protection against it.

## Why it matters

The skipped step is usually the one that shows the user the outcome — the
validation message, the confirmation, the score. The interaction still "works",
so it passes a click-based test suite; only keyboard users see the missing state,
which makes it a durable accessibility bug rather than an obvious crash.

## How to apply

- Work out which of the two you have first. The tools are not interchangeable,
  and each is a no-op against the other case.
- Against a *second listener*: `stopPropagation()` in the inner handler once it
  has fully handled the key. `preventDefault()` does nothing here — it suppresses
  the default action, not propagation to your own listeners.
- Against a *focused control's default action*: `preventDefault()` and do the
  work in your handler. This is the case where it is exactly right, and it makes
  the path testable besides — dispatched `KeyboardEvent`s run no default action,
  so a design leaning on native activation behaves one way for people and another
  under automation. Returning early when the target is the button also works,
  but only for real presses.
- Prefer capturing "which step is this key for" from the event's target rather
  than from mutable app state, when one global handler serves several steps.
- The same trap applies to click delegation, and to any state machine advanced
  from more than one point on the propagation path.
