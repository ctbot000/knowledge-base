---
title: Two Puppeteer touchStart calls 40 ms apart can reach the page 450 ms apart, so a long-press timer can fire between them
tags: [testing, automation, puppeteer, touch, ci]
added: 2026-10-05
---

## Fact

Each `touchStart()` resolves only once the page has handled it, and a page
drawing in software (CI) answers between slow frames. With a `delay(40)` between
two `touchStart()` calls, a capturing `pointerdown` listener in the page saw the
two fingers land 144-441 ms apart across eight runs slowed to CI speed (median
about 210 ms), with up to 670 ms between frames.

## Why it matters

A press-and-hold timer of 400-500 ms (hold to keep building, long-press menus)
races with the second finger of a pinch. When the page gets that finger after
the deadline and a frame runs in between, the one-finger action fires and an
assertion that a pinch does nothing fails, with a count of 1, in CI only. Locally
the gap is tens of milliseconds. The slowed runs passed at 441 ms only because
no frame happened to run in the 21 ms after the deadline, so the test sat at
the edge, not safely inside it.

## How to apply

- Measure instead of guessing: log `performance.now()` in a capturing
  `pointerdown` listener, run the test slowed ([[taskpolicy-slows-a-browser-to-ci-speed]]),
  and compare the gap with the timer.
- Take the timer out of the race from inside the page: a `pointerdown` listener
  on `window` (bubble phase) runs right after the app's own handler in the same
  dispatch, so it can push the pending deadline out with no gap to lose. Wait
  until the app has registered both fingers, assert that the hold is gone, then
  remove the listener.
- Check the fix with a deliberately long delay (900 ms): the unfixed test fails
  every time, the fixed one passes.

Related: [[puppeteer-touch-move-resolves-before-the-page-handles-it]],
[[puppeteer-touch-handles-for-multi-finger-gestures]].
