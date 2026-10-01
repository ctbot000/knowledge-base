---
title: Puppeteer's setViewport reloads the page whenever isMobile or hasTouch changes
tags: [testing, automation, puppeteer]
added: 2026-10-02
sources:
  - https://pptr.dev/api/puppeteer.page.setviewport
  - https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/cdp/EmulationManager.ts
---

## Fact

`page.setViewport()` compares `isMobile` and `hasTouch` with the page's current
emulation and, if either differs, ends by calling `page.reload()`. The
documentation only says this happens "in certain cases". Changing just `width`,
`height` or `deviceScaleFactor` never reloads.

## Why it matters

- Switching a page into or out of phone emulation mid-test throws away
  everything the app held in memory: a game in progress, an open dialog, a
  filled form. The page is back at its start screen and nothing reports it.
- Before the first `goto` the reload re-creates `about:blank`, and scripts
  registered with `evaluateOnNewDocument` run there. That document has an
  opaque origin, so touching `localStorage` throws `SecurityError: ... Access
  is denied for this document`, which arrives as a `pageerror` and fails any
  "no page errors" assertion.

## How to apply

- Pick `isMobile` and `hasTouch` once per page, before navigating, then sweep
  screen sizes with `setViewport({ width, height })` and those two unchanged.
- Size media queries (`width`, `height`, `aspect-ratio`) need no mobile
  emulation at all; only `pointer`/`hover` queries and meta-viewport layout do.
- Guard init scripts that use storage: wrap them in `try { … } catch {}`, or
  return early when `location.protocol === 'about:'`.
