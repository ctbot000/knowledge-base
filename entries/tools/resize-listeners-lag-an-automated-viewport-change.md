---
title: Right after an automated viewport change, layout is new but the page's resize listeners have not run
tags: [testing, automation, browser, puppeteer]
added: 2026-10-02
sources:
  - https://html.spec.whatwg.org/multipage/webappapis.html#update-the-rendering
  - https://drafts.csswg.org/cssom-view/#run-the-resize-steps
---

## Fact

`resize` is not dispatched when the viewport changes but in the event loop's
next "update the rendering" step. Code evaluated straight after Puppeteer's
`setViewport` already sees the new `innerWidth`, `innerHeight` and CSS layout,
while everything the page's resize handlers maintain (a canvas's drawing
buffer, a camera's aspect ratio, cached measurements) still has the old values.

A synchronous loop inside one evaluate call, such as stepping a game N frames,
never yields to the event loop, so all of it runs in that half-resized state.

## Why it matters

The result is wrong in a plausible way: a 3D view projected with the previous
aspect ratio onto the new canvas size comes out stretched sideways, and
measurements fail by tens of pixels as if the framing code were broken. Only
automation is fast enough to act in that gap; a person never sees it.

## How to apply

- After changing the viewport, wait for the app's own resized state before
  driving it, e.g. `waitForFunction` until the camera's aspect equals
  `innerWidth / innerHeight`, or for a `resize` listener added beforehand.
- Suspect this first when a measurement is off only right after a resize.
- Changing `isMobile` or `hasTouch` at the same time reloads the page instead;
  see [[puppeteer-setviewport-reloads-on-mobile-or-touch-change]].
