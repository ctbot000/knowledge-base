---
title: One key press runs two steps when a bubbling handler reads state an inner handler just changed
tags: [dom, events, keyboard, frontend]
added: 2026-08-27
---

## Fact

Event dispatch is synchronous, and a handler that mutates application state
mutates it *before* the event reaches the remaining handlers on the propagation
path. A document-level handler written as "if the answer is already submitted,
advance to the next step" therefore fires on the very key press that submitted
the answer — the inner handler flipped the flag microseconds earlier in the same
dispatch.

The result is a single key press performing two steps: submit and advance, open
and close, add and confirm. Moving focus in the inner handler makes it worse,
because the newly focused control also has native keyboard activation.

## Why it matters

The skipped step is usually the one that shows the user the outcome — the
validation message, the confirmation, the score. The interaction still "works",
so it passes a click-based test suite; only keyboard users see the missing state,
which makes it a durable accessibility bug rather than an obvious crash.

## How to apply

- Call `stopPropagation()` in the inner handler when it has fully handled the
  key. This is the direct fix: the delegated handler never sees the event, so it
  cannot act on the state that was just changed.
- Do not rely on `preventDefault()` for this — it suppresses the browser's
  default action, not the propagation to your own listeners.
- Prefer capturing "which step is this key for" from the event's target rather
  than from mutable app state, when a single global handler must serve several
  steps.
- The same trap applies to click delegation, and to any state machine advanced
  from more than one point on the propagation path.
