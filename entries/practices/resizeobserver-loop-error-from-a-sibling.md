---
title: A ResizeObserver callback that resizes another observed box no deeper in the DOM raises a loop error
tags: [resize-observer, browser, dom, css]
added: 2026-10-02
sources:
  - https://drafts.csswg.org/resize-observer/#html-event-loop
  - https://w3c.github.io/IntersectionObserver/#update-intersection-observations-algo
---

## Fact

Within one rendering update, after delivering resize observations the browser
goes on to deliver only those of targets deeper in the DOM than the shallowest
target it just delivered. When a callback changes the size of an observed
element at that depth or above, typically by setting a custom property the
other element is sized from, that observation is held over to the next frame
and `ResizeObserver loop completed with undelivered notifications` is reported.
A target deeper than the first is delivered in the same update, without error.

## Why it matters

Chrome (154) dispatches the error only to `window` `error` listeners: nothing
reaches the console or the DevTools protocol, so Puppeteer's `pageerror` never
fires and a suite asserting no page errors still passes. Error-reporting
scripts do catch it, and the dependent callback runs a frame late.

## How to apply

- To act on the size of a box that other observers' callbacks change, observe
  a deeper element, or use an `IntersectionObserver` with the box as `root`: it
  reports children the box no longer fits whole (for example, lines to drop
  from a log a shrinking room clips) asynchronously, with no loop limit.
- In a test, catch it in the page: add a `window` `error` listener in an init
  script and assert that it heard nothing.
