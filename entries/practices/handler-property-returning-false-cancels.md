---
title: An on-event handler property that returns false cancels the event, so `onkeydown = (e) => cond && act()` eats every key
tags: [dom, events, keyboard]
added: 2026-10-17
sources:
  - https://html.spec.whatwg.org/multipage/webappapis.html#the-event-handler-processing-algorithm
---

## Fact

For an event handler set as a property or attribute (`el.onkeydown = fn`,
`onclick="..."`), a return value of exactly `false` makes the browser call
`preventDefault()` (for `onerror` on window, `true` does). An arrow function
written as `(e) => e.key === 'Enter' && submit()` returns `false` for every
other key. `addEventListener` callbacks ignore their return value.

## Why it matters

The input looks focused and enabled, but nothing typed appears: every
keystroke's default action (inserting the character) is cancelled. Synthetic
typing in tests fails the same way, so it reads as a focus or automation
problem rather than a one-line handler.

## How to apply

- Give handler properties a block body, or use `addEventListener`.
- Lint for it: `no-return-assign`-style rules do not catch it; a code review
  rule of "no expression-bodied arrow on an `on*` property" does.
