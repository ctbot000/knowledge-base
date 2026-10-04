---
title: A Puppeteer touch move can resolve before the page has handled it
tags: [testing, automation, puppeteer, touch, ci]
added: 2026-10-05
---

## Fact

`TouchHandle.move()` (CDP `Input.dispatchTouchEvent`, `touchMove`) can
resolve before the page's handlers have run for that move: Chrome hands touch
moves to the page with the next animation frame. When frames are held back, as
with a software GPU in CI, a `page.evaluate` straight after it can run first
and see the state one move behind. The finger's next discrete event, such as
its `end()`, delivers the queued move before itself.

## Why it matters

A gesture test passes locally, where frames come quickly, and fails in CI on
an assertion that compares state across the last move. One move behind is a
plausible value (a zoom one step short), so it reads as an app bug. On a bare
WebGL page with a software GPU, a read straight after `move()` missed it about
one time in ten; on a heavy WebGL page, every time. `page.mouse.move()` was
always delivered in the same runs.

## How to apply

- After the last `move()`, wait for the state the gesture should end in
  (`waitForFunction`), or for the app to have handled a following `end()`.
  Never read it straight away, or after a fixed delay.
- Reproduce with CI's slowdown before trusting the fix:
  [[taskpolicy-slows-a-browser-to-ci-speed]].

Related: [[puppeteer-touch-handles-for-multi-finger-gestures]].
