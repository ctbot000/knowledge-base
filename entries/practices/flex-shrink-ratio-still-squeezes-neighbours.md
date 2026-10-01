---
title: A large flex-shrink on one item still takes a fraction of a pixel from its neighbours, enough for an ellipsis
tags: [css, flexbox, typography]
added: 2026-10-02
sources:
  - https://www.w3.org/TR/css-flexbox-1/#resolve-flexible-lengths
---

## Fact

A shortfall is shared out in proportion to `flex-shrink` times the flex base
size, so `flex-shrink: 1000` on a long message still leaves its short
neighbour a sliver of it: 0.05 px in Chrome 154. A neighbour sized to its text
with `text-overflow: ellipsis` needs no more than that to end in "…".

## Why it matters

The obvious way to say "this item gives way first" fails in the very case it
was written for: the neighbour's text (an ID, a code, a name) loses its last
character, and checks with `scrollWidth` do not notice
([sub-pixel overflow hides from scrollWidth](subpixel-overflow-hides-from-scrollwidth.md)).

## How to apply

Let the yielding item take only the room that is left instead of shrinking:

```css
.message { flex: 1000 1 0; min-width: 0; max-width: max-content; }
```

Its base size is 0, so it never adds to the shortfall; it grows into the free
space up to its own content width, and the large grow factor puts it ahead of
a `flex: 1` filler beside it. Or give the protected item `flex-shrink: 0`
where the row is known to have room for it.
