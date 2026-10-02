---
title: Right after a viewport or layout change, what resize listeners and ResizeObservers maintain is still stale
tags: [testing, automation, browser, puppeteer]
added: 2026-10-02
updated: 2026-10-02
sources:
  - https://html.spec.whatwg.org/multipage/webappapis.html#update-the-rendering
  - https://drafts.csswg.org/cssom-view/#run-the-resize-steps
  - https://drafts.csswg.org/resize-observer/#html-event-loop
---

## Fact

`resize` events and ResizeObserver callbacks run in the event loop's next
"update the rendering" step, not when the size changes. Code evaluated straight
after Puppeteer's `setViewport`, or in the same task as a DOM change that
resizes an observed box, already sees the new layout (`innerWidth`,
`offsetHeight`), while everything those callbacks maintain (a canvas's drawing
buffer, a camera's aspect ratio, a CSS custom property other elements are
positioned from) still holds the old value. Observers run after that frame's
requestAnimationFrame callbacks, so code resumed by one awaited rAF still sees
the old value; after a second it is current.

A synchronous loop inside one evaluate call, such as stepping a game N frames,
never yields to the event loop, so all of it runs in that half-updated state.

## Why it matters

The result is wrong in a plausible way: a 3D view projected with the previous
aspect ratio comes out stretched sideways, and controls positioned from an
observed height overlap what they were moved to clear, by exactly the change.
Both callbacks run before paint, so a person never sees it; only automation is
fast enough to measure in the gap.

## How to apply

- After a resize, or a change that resizes an observed box, wait for the app's
  own updated state: `waitForFunction` until the camera's aspect equals
  `innerWidth / innerHeight`, or until the custom property equals the box's size.
- Suspect this first when a measurement is off only right after a change.
- Changing `isMobile` or `hasTouch` at the same time reloads the page instead;
  see [[puppeteer-setviewport-reloads-on-mobile-or-touch-change]].
