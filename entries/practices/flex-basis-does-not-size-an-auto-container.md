---
title: A shrinkable flex item contributes its content width, not its flex-basis, to an auto-sized container
tags: [css, flexbox, layout]
added: 2026-09-01
sources:
  - https://www.w3.org/TR/css-flexbox-1/#intrinsic-sizes
  - https://developer.mozilla.org/en-US/docs/Web/CSS/flex-basis
---

## Fact

When a flex container is sized by its own content — it is itself a flex item
with `flex: 0 1 auto`, or simply `width: auto` — the intrinsic size it computes
from an item declared `flex: 0 1 190px` is the item's **content** width, not
190px. Because the item is shrinkable, its max-content contribution is clamped
down to what it actually contains.

The item then sits inside a container narrower than its own basis, so it shrinks
to fit, and a preferred width of 190px renders as 116px of text. Giving the item
`width: 190px` (with `flex: 0 1 auto`) makes the same layout come out at 190px
and still shrink when space runs short.

## Why it matters

This is the standard tab-strip or chip-row layout: fixed preferred width, all
items shrinking together once the row fills. Written with `flex-basis` it looks
correct at every stage of development — items are equal, they shrink under
pressure, nothing overflows — and is simply the wrong size, sized by whatever
text happens to be in them. Nothing in the box model points at `flex-basis`,
because the value is being honoured; it is the container that never asked for
it.

## How to apply

- Express a fixed preferred size with `width` (or `height` in a column) and keep
  `flex: 0 1 auto`. Reserve `flex-basis` for items in a container whose size is
  already determined from the outside.
- Or set `flex-shrink: 0` on the item and let the container clip or scroll; a
  non-shrinkable item does contribute its basis.
- Verify with `offsetWidth` at two and at a dozen items rather than by eye —
  equal-but-wrong widths look right in a screenshot.
