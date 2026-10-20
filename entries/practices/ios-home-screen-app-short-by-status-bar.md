---
title: An iOS Home Screen web app with a translucent status bar is short by the bar's height, and only growing the root element fixes it
tags: [ios, ipad, pwa, standalone, css, safe-area, webkit]
added: 2026-10-20
sources:
  - https://bugs.webkit.org/show_bug.cgi?id=254868
  - https://dev.to/karmasakshi/make-your-pwas-look-handsome-on-ios-1o08
---

## Fact

With `apple-mobile-web-app-status-bar-style: black-translucent` and
`viewport-fit=cover`, a page opened from the iOS/iPadOS Home Screen starts under
the status bar, yet the initial containing block, `100%`, `inset: 0` and fixed
elements all end `env(safe-area-inset-top)` short of the bottom, leaving an empty
strip. Measured on iPadOS 26: page 802 on an 834 screen, inset 32; `100vh` was
shorter still (777), and `(display-mode: standalone)` did not match at all
(no manifest, only the apple meta tag).

## Why it matters

The obvious fixes fail. A `display-mode` media query never applies; `100vh`
makes it worse; fixed layers given `calc(100% + inset)` are laid out to the
bottom but still not painted past the strip. Growing `html` does paint to the
bottom, and fixed elements' containing block grows with it, so growing both
adds the gap twice and pushes bottom UI off screen.

## How to apply

- Detect with `navigator.standalone === true`, not `display-mode`.
- Grow only the root: `html { height: calc(100% + var(--gap, 0px)) }`, leave
  fixed layers at `inset: 0`.
- Set `--gap` from JS: reset it to 0, measure a `position: fixed; inset: 0`
  probe carrying `padding-top: env(safe-area-inset-top)`, and use the inset only
  when screen height minus the probe's height equals it (and the probe spans the
  screen's width, so split view is left alone). Re-run on `resize`. Measuring with
  the gap applied feeds back on itself.
- Verify on a device: desktop Chrome cannot emulate standalone or the insets.
