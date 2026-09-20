---
title: A grid or flex item sized with width:100% overflows by exactly its own margin
tags: [css, grid, layout]
added: 2026-09-20
sources:
  - https://drafts.csswg.org/css-align/#valdef-justify-self-stretch
---

## Fact

Default `stretch` alignment sizes an item to the track **minus its margins**.
`width: 100%` resolves against the containing block and subtracts nothing, so the
two agree only while the margin is zero. In a 300px track, with `margin-left: 40px`:

| declaration | resulting width |
| --- | --- |
| `width: auto` (stretch) | 260px |
| `width: 100%` | 300px — overflows by 40px |

A replaced-looking element is not an exception: a `<button>` as a grid item
stretches to 260px on its own.

## Why it matters

`width: 100%` is the reflex for "make this button fill the row", because buttons
are `inline-block` in normal flow and do not stretch there. Inside a grid or flex
container they already do, so the declaration is redundant — and the moment any
one item gets an indent (`.nested { margin-left: 1.1rem }`), that item alone
pushes past the edge.

It reads as a margin bug in one variant, not as a width rule applied to the whole
class. Page padding usually absorbs most of the excess, so what surfaces is a
one- or two-pixel horizontal scroll at narrow widths rather than an obvious
misalignment.

## How to apply

- Do not set `width: 100%` on a grid or flex item; let `stretch` do it.
- Keep it only where you deliberately want the margin to overflow, or pair it
  with `box-sizing: border-box` and padding instead of margin.
- Hunting a few pixels of horizontal scroll: compare each descendant's
  `getBoundingClientRect().right` against `documentElement.clientWidth`, then
  check whether the offender declares an explicit width.
