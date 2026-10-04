---
title: Every way a press can end has to send its release, or a hold it started keeps repeating
tags: [dom, events, pointer-events, touch, ui]
added: 2026-10-05
---

## Fact

When pressing starts something and releasing stops it (hold to repeat, a
long-press timer, a held tool), pointerup is only one of the ways a press ends.
A second finger turning it into a pinch, focus loss or a hidden page, and a
pointercancel end it too. Handling those by flagging the press as a drag
(`press.moved = true`) or forgetting it (`press = null`) does stop the tap, but
the release never reaches whatever the press started, so the repeat keeps
firing: at the first finger's spot for as long as the pinch lasts, or by
itself after a blur until the next press.

## Why it matters

It reads as the gesture doing the wrong thing ("pinching also builds"), so the
search goes to the pinch maths. One-finger taps and drags, and a quick pinch,
all pass; it takes two fingers held longer than the hold delay.

## How to apply

- One `endPress()` that clears the record *and* emits the release; call it
  from every path that abandons a press: a second finger landing, blur and
  `visibilitychange`, pointercancel.
- While two or more fingers are down, no finger starts a press: test
  `size >= 2`, not `=== 2`, or a third finger (a resting palm) starts one
  mid-pinch.
- When a pinch ends with one finger still down, start a fresh drag from that
  finger's current position, already past the tap threshold. A drag record kept
  from before the pinch turns the view by everything the finger travelled
  during it.
- Test with real multi-touch, holding the pinch past the hold delay, and count
  the uses of the action rather than looking at the result of one.

Related: [[gesture-completion-belongs-to-its-press]], [[puppeteer-touch-handles-for-multi-finger-gestures]].
