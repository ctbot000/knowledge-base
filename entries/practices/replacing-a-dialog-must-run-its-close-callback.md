---
title: A dialog opened over another must run the replaced one's close callback first
tags: [ui, dialogs, state, frontend]
added: 2026-10-02
---

## Fact

A UI with one dialog slot usually stores the open dialog's `onClose` and runs
it from `close()`. If `open()` simply overwrites that slot, a dialog opened
while another is showing replaces it without its cleanup ever running: whatever
the first one changed when it opened (a camera, a mode, a timer, a canvas being
drawn into) stays changed, and no dialog is left that can undo it.

## Why it matters

It looks like a corner case until a dialog does not block the page. A
see-through dialog or side sheet (`pointer-events: none` on its backdrop)
leaves every other button that opens a dialog clickable, so "open while open"
is an ordinary click, and only at the screen sizes where those buttons are
neither hidden nor under the panel. The symptom shows up later, on another
screen, as a state nothing on it explains.

## How to apply

- In `open()`, take the current `onClose`, clear the slot, then call it, all
  before building the new dialog. Not after: the new dialog may set up the very
  state the old cleanup resets (opening the same dialog again is the simple
  case), and a cleanup run afterwards undoes it.
- Calling `close()` from `open()` works too, if its other effects (a sound,
  returning focus, re-enabling input) are harmless in between.
- Test it with a real pointer click on an opener beside the open dialog, at a
  size where one is reachable: [[element-click-does-not-hit-test]].
