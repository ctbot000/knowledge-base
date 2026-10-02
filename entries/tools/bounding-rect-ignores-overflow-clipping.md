---
title: getBoundingClientRect ignores overflow clipping, so an overlap check flags children scrolled out of sight
tags: [testing, automation, dom, css]
added: 2026-10-02
sources:
  - https://drafts.csswg.org/cssom-view/#dom-element-getboundingclientrect
  - https://w3c.github.io/IntersectionObserver/#calculate-intersection-rect-algo
---

## Fact

`getBoundingClientRect()` returns an element's border box where layout put it,
whether or not an ancestor with `overflow` other than `visible` clips it. An item
scrolled out of a scroll container still reports a rect past the container's
edge: over whatever sits beside the container, or off screen.

## Why it matters

A layout test that sweeps boxes for overlaps ("no button covers an item in the
row") starts failing when a wrapping row becomes a sideways scroller: the hidden
items lie, by their rects, under the buttons beside the row, though nothing is
drawn there. The same blind spot lets an "is it on screen" check pass for an item
that is entirely clipped.

## How to apply

Compare what shows: intersect the item's rect with the clip rect of each
clipping ancestor, and skip it when nothing is left.

```js
const c = container.getBoundingClientRect(); // its padding box, if it has no border
const r = item.getBoundingClientRect();
const shown = { left: Math.max(r.left, c.left), right: Math.min(r.right, c.right),
                top: Math.max(r.top, c.top), bottom: Math.min(r.bottom, c.bottom) };
if (shown.left < shown.right && shown.top < shown.bottom) check(shown);
```

With a border or a scrollbar, build the clip rect from `clientLeft`,
`clientTop`, `clientWidth` and `clientHeight` instead. A sideways scroller clips
vertically too: `overflow-x: auto` turns `overflow-y: visible` into `auto`.
`IntersectionObserver`'s `intersectionRect` does apply ancestors' clips, but only
asynchronously. Scrolled items pass through the container's box, so checking
that box as well covers every scroll position.
