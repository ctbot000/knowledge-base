---
title: A shrink-to-fit box whose flex row wraps is as wide as its limit, not its longest line
tags: [css, flexbox, layout, pointer-events]
added: 2026-10-02
sources:
  - https://www.w3.org/TR/css-sizing-3/#fit-content-size
  - https://www.w3.org/TR/CSS2/visudet.html#shrink-to-fit-float
---

## Fact

A box that sizes to its content (absolutely positioned, floated, inline-block,
or `width: fit-content`) takes `min(max-content, available)`. Once its flex row
or its text has to wrap, max-content is the unwrapped length, so the box takes
the whole available width or `max-width`, and every line is shorter than the
box. Two 162px items under `max-width: 200px` give a 200px box with an empty
strip beside each line, and `width: fit-content` changes nothing.

## Why it matters

The empty strip is still part of the box. In an overlay over a canvas or a map
it catches the taps and clicks that seem to land on the scene beside the
controls, but only on screens where the row wraps, so a wide layout never
shows the problem. A background or border on the container shows the same
strip as a visible gap.

## How to apply

- Give the wrapping container `pointer-events: none` and its items
  `pointer-events: auto`. Put backgrounds and borders on the items.
- When the limit means "stop short of a neighbour", setting both `left` and
  `right` costs nothing over `max-width`: the box fills the space either way
  once anything wraps.
- Test with `elementFromPoint` just past the end of the last line. It should
  return whatever is behind, not the container. The same trap with 3D wrappers
  is described in [[preserve-3d-scaffolding-eats-the-pointer]].
