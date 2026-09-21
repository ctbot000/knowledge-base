---
title: A screenshot taken right after a state change captures the transition, not the new state
tags: [testing, automation, browser]
added: 2026-09-21
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions/Using_CSS_transitions
---

## Fact

Automation drives a UI far faster than a human does. An action and the screenshot
that checks it land in the same few milliseconds, so anything animated is caught
part-way: a cross-fade between two panels shows *both*, a slide-in shows the
element off its final position, a fade-out shows content that the app has already
switched away from.

The DOM is already correct at that moment. Only the paint is in between.

## Why it matters

The half-rendered frame is a plausible picture of a real bug, and it names the
wrong culprit. Two panels visible at once reads as "the switch does not hide the
old one" — so the hunt starts in the toggling logic, which is fine. A sequence of
such screenshots is worse still: each one looks consistently broken, which feels
like confirmation rather than the same 300 ms repeated.

It is also invisible in review. The transition is an aesthetic line in a
stylesheet, usually written by someone else, and nothing in the failing screenshot
points at it.

## How to apply

- Assert on the DOM, not on pixels: read the class list, `getComputedStyle`, or
  the accessibility tree. These are already final when the action returns.
- When a screenshot is the point, wait past the longest transition first — grep
  the stylesheet for the duration rather than guessing, and add a margin.
- For a whole suite, disable animation globally instead of sleeping everywhere:
  inject `* { transition: none !important; animation: none !important; }`, or
  drive the page under an emulated `prefers-reduced-motion: reduce`.
- Suspect this first whenever a screenshot shows *two* states of the same widget.
