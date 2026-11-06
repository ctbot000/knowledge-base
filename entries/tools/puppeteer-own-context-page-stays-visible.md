---
title: A Puppeteer page in its own browser context stays visible and keeps getting frames, whatever is in front
tags: [testing, automation, browser, puppeteer]
added: 2026-11-06
---

## Fact

Only tabs sharing a browser context hide each other. A page behind another in the
same context reports `visibilityState === 'hidden'` and gets no animation frames;
a page opened with `createBrowserContext()` reports `visible` and runs at full
frame rate no matter which page was brought to the front.

## Why it matters

A multi-player test usually gives each player a context of their own, for separate
storage. Every page's loop then runs on the wall clock at once. A test that steps
one page by hand, believing it frozen behind the other, is stepping on top of its
real frames, so anything that ends by game time (a timer running out, a round
being lost) can end between two evaluate calls, and only on a loaded machine where
those calls are slow.

## How to apply

- Do not rely on `bringToFront()` to pause a page in another context.
- Keep whatever must not time out alive from a loop inside the page (a
  `requestAnimationFrame` callback playing the part), or stub out its clock, rather
  than racing it from the test.
- For the opposite case, a page that really is hidden and never advances, see
  [[hidden-surface-delivers-no-frames]].
