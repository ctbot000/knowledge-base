---
title: elementFromPoint skips pointer-events:none layers, so it cannot tell which of two tap-through overlays is drawn on top
tags: [testing, automation, dom, css]
added: 2026-10-02
sources:
  - https://drafts.csswg.org/cssom-view/#dom-document-elementfrompoint
---

## Fact

`document.elementFromPoint()` and `elementsFromPoint()` are hit tests, not paint
queries. An element with `pointer-events: none`, and everything inside it that
inherits the value, is left out. A HUD, a status banner, a thumbstick graphic or
a toast layer made tap-through, so that touches reach the canvas below, is never
returned: both calls answer with whatever lies underneath it.

## Why it matters

A test asking whether a message is drawn over the control it overlaps, or under
it, gets the canvas back either way, so it reports nothing about the stacking.
Bounding-box overlap cannot answer it either, and the difference is the point:
text drawn over a translucent ring reads fine, while the same text with the ring
drawn over it is crossed out.

## How to apply

Let both layers take the pointer for the duration of one hit test, in the middle
of where they meet, then restore them:

```js
a.style.pointerEvents = b.style.pointerEvents = 'auto';
const top = document.elementFromPoint(x, y); // whichever of the two is drawn on top
a.style.pointerEvents = b.style.pointerEvents = ''; // or their previous inline values
const aOnTop = a.contains(top);
```

An inline `auto` overrides a `none` inherited from a tap-through container, so it
works for one element inside a HUD too. Anything hit-testable drawn above both
still wins, so pick a point that only the two share. Whether a real control can
be reached is a separate check: [[element-click-does-not-hit-test]].
