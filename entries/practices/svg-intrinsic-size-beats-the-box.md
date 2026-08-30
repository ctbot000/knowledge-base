---
title: An inline SVG sizes itself from its viewBox unless both axes are definite
tags: [css, svg, layout, frontend]
added: 2026-08-30
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Replaced_element
  - https://www.w3.org/TR/CSS21/visudet.html#abs-replaced-width
---

## Fact

An `<svg>` is a replaced element, and a `viewBox` gives it an intrinsic aspect
ratio. Layout keeps consulting that ratio wherever the CSS leaves either axis
open, and the ratio wins over the box the surrounding rules seem to describe.

Two places this bites:

- **A `1fr` track is `minmax(auto, 1fr)`.** The auto minimum is the item's
  min-content size, which the SVG derives from its ratio, so a grid of square
  cells silently stretches to the tallest bottle-shaped child.
- **Insets do not size a replaced element.** With `position:absolute`, all four
  offsets set and `width`/`height` auto, the width comes from `left`/`right`,
  the height comes from the ratio, and `bottom` is simply ignored — the element
  overflows its own inset box.

## Why it matters

The overflow is painted under whatever comes later in the DOM, so the symptom is
not "this element is too big" but "the row below is covering mine" — a
z-order-looking bug in a layout that is actually mis-sized. It also scales with
content: one oddly-proportioned icon widens every track in the grid.

## How to apply

- Write grid tracks as `repeat(n, minmax(0, 1fr))` whenever a cell holds
  anything with an intrinsic ratio.
- Give the SVG a definite box on both axes rather than trusting insets:
  `width:calc(100% - 6px); height:calc(100% - 14px)`, or wrap it in a
  non-replaced element that the insets can size and let the SVG fill that.
- `preserveAspectRatio` (default `xMidYMid meet`) then letterboxes the drawing
  inside whatever box you gave it, which is usually the intent anyway.
