---
title: An armed-tool mode that survives its own success turns every later click into a refusal
tags: [ui, interaction-design, frontend]
added: 2026-09-13
---

## Fact

Select-then-apply interfaces — an inventory item you are carrying, a format
painter, a stamp tool, "add connection" mode — hold a mode between two clicks.
If the mode is not cleared when the apply *succeeds*, it is still armed for the
next click, and that click is no longer the plain action the user meant.

The tell is that nothing looks broken at the moment of use. The tool worked, the
message was right. The damage lands one click later, and it arrives as a
plausible sentence about the target rather than as an error:

> The box of matches does nothing for the mail sacks.

## Why it matters

The user reads that as a statement about the *target*: wrong place, wrong thing,
try somewhere else. So they go hunting for a better target, and every click they
try produces another confident refusal, because the fault is in a mode they have
no reason to suspect. A room, a canvas, a diagram can be made to feel hostile by
one missing line.

Tests miss it for the same reason. A test that applies the tool and asserts the
effect stops exactly one step before the bug; only a test that performs an
*unrelated* action afterwards sees it.

## How to apply

- Disarm on success by default, and make staying armed the explicit exception —
  a flag on the result for the cases where the thing really does stay in the
  hand (a can that is now full, a brush someone is repeat-applying).
- Put the exception in the shared dispatcher, not in each call site. Each site
  forgetting it is the whole failure mode.
- Show the armed state where the eye is: the cursor, the hover target, a class
  on the surface. A mode nobody can see is a mode nobody will think to clear.
- Give it an escape: `Esc`, and clicking the source again.
- Test the click *after* the successful one, not just the successful one.
