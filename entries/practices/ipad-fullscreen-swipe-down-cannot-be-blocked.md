---
title: On an iPad any swipe down leaves element full screen, and no page can stop it
tags: [fullscreen, ios, ipad, webkit, touch, games]
added: 2026-10-12
sources:
  - https://github.com/WebKit/WebKit/blob/main/Source/WebKit/UIProcess/ios/fullscreen/WKFullScreenWindowControllerIOS.mm
  - https://itch.io/t/4160298/ipad-touch-gesture-challenges-preventing-the-dreaded-fullscreen-swipe-down
---

## Fact

iPadOS WebKit (Safari, and Chrome, Edge and every other iPad browser, which all
use it) puts a native `UISwipeGestureRecognizer` (direction down, one finger) and
a pan recognizer on the full screen view itself. They recognize simultaneously
with everything and never ask the page, so `preventDefault()` on touch events,
`touch-action: none` and `overscroll-behavior` do not stop a downward swipe
anywhere on screen from exiting `requestFullscreen()`.

## Why it matters

A game or drawing app played by dragging drops out of full screen at the first
downward stroke, which makes the page's full screen button worse than useless.
Time spent on touch handlers to block it is wasted.

## How to apply

- On iPads, do not offer `requestFullscreen()` for drag-driven content. Offer
  the Home Screen instead (`apple-mobile-web-app-capable`, or a manifest with
  `display: standalone`); a standalone web app has no swipe-to-exit. Third-party
  iPad browsers can add to the Home Screen too (iPadOS 16.4+).
- Detect an iPad by its touch screen, not its user agent: by default it asks for
  desktop pages and reports a Mac.
  `/iPad/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)`
- Opened from the Home Screen, `navigator.standalone === true`: hide the button.
