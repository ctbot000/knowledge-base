---
title: Fitting text into a narrowing shape needs a search over wrap width, not just font size
tags: [css, typography, layout]
added: 2026-09-08
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Range/getClientRects
---

## Fact

When a block of text has to sit inside a shape that narrows — a triangle, a
circle, a bubble with a tail — shrinking the font until it fits does not
converge. A smaller font wraps into *fewer, longer* lines, and a long line is
exactly what the narrow end of the shape cannot accept. The loop bottoms out at
its minimum size with the text still sticking out of the sides.

Font size and wrap width are one coupled pair: the size that fits depends on how
many lines the text breaks into, and that depends on the width it is allowed to
occupy. Only a search over both finds the fit.

## Why it matters

The single-variable loop looks correct and fails silently, so the bug gets
attributed to the shape — a wrong `clip-path`, a bad aspect ratio — rather than
to a missing degree of freedom. Clipping the text with the shape makes it worse:
the overflow becomes invisible rather than absent, and a long phrase loses its
first and last letters with nothing in the console.

## How to apply

- Anchor the text block at the shape's **wide** end and let it grow toward the
  narrow one, so extra lines move into more room, not less.
- Search font size descending; at each size try a few candidate wrap widths,
  ordered by looks rather than by size — a middle width usually yields the most
  balanced block.
- Test **per line box**, not per block: `range.selectNodeContents(el)` and
  `range.getClientRects()` give one rect per line. A line fits when its half
  width clears the shape's half width at that line's own top edge, which is
  where the shape is narrowest for that line.
- Compare in fractions of the shape's box. Both the box and the line rects carry
  any in-flight transform equally, so the test stays valid mid-animation.
- Draw the shape as its own layer instead of clipping the text with it: a fit
  that is slightly off then degrades to a little overflow instead of to missing
  words.
