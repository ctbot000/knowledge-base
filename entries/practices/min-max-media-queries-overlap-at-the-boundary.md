---
title: A min- and a max- media query on the same value both match at that value, so opposite breakpoints overlap at one exact size
tags: [css, responsive, media-queries]
added: 2026-10-02
updated: 2026-10-02
sources:
  - https://www.w3.org/TR/mediaqueries-4/#mq-min-max
  - https://www.w3.org/TR/mediaqueries-4/#mq-range-context
  - https://www.w3.org/TR/mediaqueries-4/#mq-not
---

## Fact

`min-*` and `max-*` media features are inclusive (≥ and ≤). A pair written as
opposites, such as `(max-width: 760px)` and `(min-width: 760px)`, or
`(max-aspect-ratio: 3/4)` and `(min-aspect-ratio: 3/4)`, both match when the
viewport is exactly on the boundary. Every rule in both blocks applies there, and
where they disagree the later block wins.

## Why it matters

The overlap is one value wide, so dragging a window never shows it, but real
devices sit on it exactly: in CSS pixels most iPads in portrait (768×1024,
810×1080, 834×1112) are exactly 3:4. A "held sideways" rule, such as one that
narrows a bottom bar to keep it clear of thumb controls in the corners, then also
runs on the upright layout, where those controls are elsewhere, and squeezes the
bar for no reason, on those sizes only.

## How to apply

- Make one side strict: range syntax `(aspect-ratio > 3/4)` or `(width > 760px)`
  (Media Queries 4: Chrome 104+, Safari 16.4+, Firefox 63+), or
  `not all and (max-aspect-ratio: 3/4)` where older engines matter.
- That leading `not` negates the whole query, so `not all and
  (max-aspect-ratio: 3/4) and (max-width: 760px)` means "not narrow and
  upright" and matches wide upright screens too. Nest the narrower `@media`
  inside it, or pick bounds that imply the side: `(min-width: 538px)` with
  `(max-height: 687px)` is already wider than 3:4.
- A width can also be nudged (`min-width: 760.02px`); a ratio cannot.
- Put the boundary itself in every viewport sweep (768×1024 for 3/4), since
  sizes either side of it pass.
