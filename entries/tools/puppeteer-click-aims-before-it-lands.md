---
title: Puppeteer aims a click where an element is when it looks, so one still animating in gets missed
tags: [testing, automation, puppeteer, css]
added: 2026-10-02
sources:
  - https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/api/ElementHandle.ts
  - https://drafts.csswg.org/web-animations-1/#dom-animatable-getanimations
---

## Fact

`ElementHandle.click()`, and `page.click()` with it, reads the element's box
first and then sends the mouse events to that point in separate protocol
calls. The hit test happens when the events arrive. If a frame in between
moves the element — a dialog popping in with a `scale()` animation is the
usual case — the press lands on whatever is at that point now, often a
neighbouring control.

Under software rendering the gap is wide and random: right after a dialog
opens, frames can take most of a second, and its pop-in stays pending at the
first keyframe across several of them, then jumps straight to the end in one.

## Why it matters

The wrong control is pressed without any error. The test then waits for an
effect nobody asked for and fails as a polling timeout on the slowest runner,
which reads as slow CI rather than a misaimed click. On a fast GPU the click
usually completes before the animation's first frame, so it rarely shows up
locally.

Comparing the element's box across two frames does not catch it: a pending
animation shows the same first-keyframe box in consecutive frames.

## How to apply

- Before clicking inside anything that animates in, wait until it has no
  animations left: `waitForFunction(() => !panel.getAnimations().length)`.
  Pending and running animations are listed; a finished one with no fill is not.
- Bring the page to the front first. A hidden page has no frames, so its
  animations never finish; see [[puppeteer-click-hangs-in-background-tab]].
- Suspect this when a click-driven step times out only on CI and the page shows
  that a different choice was made: another option picked, another switch flipped.
