---
title: A mouse-clicked helper button keeps focus, so the next Enter re-fires it instead of confirming
tags: [dom, focus, keyboard, frontend]
added: 2026-09-28
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button#clicking_and_focus
---

## Fact

Most browsers focus a `<button>` when it is clicked with the mouse; Safari
does not, by design. A page that confirms with Enter, and
correctly leaves Enter on a focused button to that button's native activation,
therefore sends the next Enter to whatever helper the user last clicked — a
+1/−1 stepper, a hint toggle — instead of to the confirm action.

## Why it matters

The confirm path works in keyboard-only testing and in Safari, and breaks only
after a mouse interaction with a secondary control. The symptom reads as a logic
bug ("Enter adds one more degree", "Enter hides the hint") rather than as focus
sitting somewhere unexpected.

## How to apply

- For controls that adjust something the user then confirms, call
  `preventDefault()` on their `mousedown`: focus stays where it was, the click
  still fires, and keyboard users can still Tab to the control.
- Or move focus back to the primary control at the end of the helper's action.
- Test the sequence "click helper, then press Enter" with real input, not a
  dispatched click: a synthetic `click()` never moves focus.

Related: [[key-event-runs-two-steps]].
