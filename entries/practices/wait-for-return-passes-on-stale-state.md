---
title: A wait for something to be back where it started passes at once if the change was never shown
tags: [testing, flaky-tests, rendering, async]
added: 2026-10-19
---

## Fact

After an action that moves something away and back (an object knocked back and
then reset, a panel closed and reopened), waiting for its shown state to equal
the starting state is already true while the display has not caught up with the
action: no frame drawn since, a freeze effect holding it, an event not yet
delivered. The wait passes, the change is shown afterwards, and the next step
acts on it.

## Why it matters

The test passes on a fast machine, where the change shows long before the wait
starts, and fails under load in the step after the wait, so the wait never looks
guilty: a click aimed at the "returned" object finds it still on its way out.

## How to apply

- First wait until the change itself has been shown (a value that differs from
  the start, or a flag only the display path clears), then wait for the return.
- Or return it to a state distinguishable from the start, so an old frame cannot
  satisfy the wait.
- To prove it, freeze the display path for a moment after the action and hold
  back the return: the old wait passes on the frozen state and the next step fails.
