---
title: A DOM-to-image snapshot draws the page's noscript content
tags: [frontend, screenshot, svg, dom]
added: 2026-10-12
sources:
  - https://github.com/qq15725/modern-screenshot/issues/71
---

## Fact

Libraries that turn the DOM into an image (modern-screenshot, html-to-image,
dom-to-image) clone the page into an SVG `<foreignObject>` and load that as an
image. An SVG image runs with scripting disabled, so every `<noscript>` element
in the clone renders, and its fallback text appears in the picture.

## Why it matters

A "this page needs JavaScript" line shows up over the top of a screenshot of a
page that is plainly running JavaScript. Nothing on screen explains it, and the
libraries do not strip `<noscript>` by default.

## How to apply

Leave `<noscript>` out with the library's node filter:

```js
domToCanvas(document.body, { filter: (node) => node.nodeName !== 'NOSCRIPT' });
```
