---
title: An absolutely positioned box centred with left 50% shrinks to fit half its container, whatever its max-width
tags: [css, layout, positioning]
added: 2026-10-02
sources:
  - https://www.w3.org/TR/CSS2/visudet.html#abs-non-replaced-width
  - https://www.w3.org/TR/css-sizing-3/#fit-content-size
---

## Fact

With `left: 50%` and `right: auto`, an absolutely positioned box of auto width
shrinks to fit the space right of its left edge: half the containing block.
It comes out `min(max(min-content, 50%), max-content)`. The
`translateX(-50%)` that centres it does not affect layout, and `max-width`
only caps. Content wider than half the container gets half the container or
its min-content width, never its max-content one, and `width: fit-content`
gives the same result.

## Why it matters

A centred bottom bar or toast wraps or scrolls while the screen has room to
spare. In a scrolling row whose min-content is a little under its max-content
(a label at the end that could wrap), the last item is cut off on every screen
narrower than twice the row: for a 750px row, everything under 1500px wide.
Phones, where the row is wider than the screen anyway, and very wide screens
look right. It reads as a bar slightly too narrow, not as a centring bug.

## How to apply

- Add `width: max-content` and keep `max-width` as the cap: the box is then
  `min(max-content, max-width)`, still centred by the transform.
- Or centre without the transform: `left: 0; right: 0; margin-inline: auto;
  width: fit-content` shrinks against the whole container.
- Either way a wrapping child makes max-content its unwrapped length, so the
  box can grow to its cap; see [[wrapped-flex-row-fills-its-limit]].
- Measure such a box on a screen between one and two times its content width;
  that is the only range where it is too narrow.
