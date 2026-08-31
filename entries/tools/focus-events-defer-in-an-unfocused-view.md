---
title: element.focus() moves activeElement but fires no focus event while the view lacks system focus
tags: [testing, automation, dom, focus]
added: 2026-09-01
sources:
  - https://html.spec.whatwg.org/multipage/interaction.html#focusing-steps
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus
---

## Fact

Calling `element.focus()` in a document that does not hold the system focus —
an embedded view whose sibling has focus, a background window, a hidden iframe —
sets `document.activeElement` immediately but defers the `focus` and `blur`
events until the document regains focus. The DOM reports the element as focused
while every handler attached to focusing it has yet to run.

## Why it matters

It breaks automation quietly and only for state that lives in the handler. A
driver that calls `focus()` and then dispatches input sees the field accept
text, so the test reads as working, while the flag the focus handler was
supposed to set is still false — and any later render, seeing "not editing",
overwrites what was typed.

The resulting failure is intermittent and unreproducible in isolation: a probe
that focuses the same field in a window that does hold focus passes every time.

## How to apply

- Focus the view before the element: in Electron `webContents.focus()`, in a
  browser `window.focus()`, and only then the field.
- Prefer real input injection for anything focus-dependent —
  `webContents.sendInputEvent` with a mouseDown/mouseUp at the element's rect
  drives the same path a person does, including the focus event.
- Assert on the handler's own state, not on `document.activeElement`, when
  checking that a focus path ran.
- Do not conclude from `activeElement` alone that focus handlers have executed.
