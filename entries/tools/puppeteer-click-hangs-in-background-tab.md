---
title: Puppeteer's click() never returns for an element in a background tab
tags: [testing, automation, puppeteer]
added: 2026-09-23
sources:
  - https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/api/ElementHandle.ts
---

## Fact

`ElementHandle.click()`, and `page.click()` with it, first calls
`scrollIntoViewIfNeeded()`, which waits for an `IntersectionObserver` callback to
measure visibility, with no timeout. A page in a background tab is hidden, and a
hidden page gets no observer callbacks, so the click waits forever without
throwing. The test runner's timeout is the first thing to fire.

## Why it matters

The pattern is common: open a second page, then go back and click in the first.
`evaluate()` and `$eval()` on that page keep working, so the hang looks like a
broken click handler or a stuck navigation rather than the click itself.

## How to apply

- `await page.bringToFront()` before clicking in a page that may not be the
  active tab.
- Or click from inside the page (`page.$eval(sel, (el) => el.click())`), which
  skips the wait but also skips hit-testing: [[element-click-does-not-hit-test]].
- The underlying rule: [[hidden-page-delivers-no-scroll-or-intersections]].
