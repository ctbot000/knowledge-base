---
title: SVG has no z-index, so a later sibling silently paints over an earlier one
tags: [svg, graphics, frontend]
added: 2026-09-16
sources:
  - https://www.w3.org/TR/SVG2/render.html#RenderingOrder
---

## Fact

SVG paints strictly in document order. `z-index` does not apply to SVG
elements, and neither does anything else that would let a later element yield to
an earlier one — the last sibling drawn wins wherever the two overlap.

Nothing reports this. The covered element is still in the DOM, still matches its
selectors, still has a `getBBox()`, still fires events where it is not covered.
The only symptom is that a human cannot see it.

## Why it matters

It silently deletes information rather than the element. Where the graphic is
decoration, the loss is cosmetic. Where the graphic *is* the data — a count to
read off, a label, a control someone has to find and click — the interface now
asks a question it has made unanswerable, and every automated test still passes
because tests assert on values, not on what is visible.

Overlap also grows with content: an element that cleared its neighbour at
authoring time will be covered the moment either one is resized, re-centred, or
given a longer string.

## How to apply

- Order deliberately: background, then scenery, then anything that must be read
  or clicked. Where two things must not collide, keep them apart by coordinates
  rather than by ordering luck.
- Assert it rather than eyeballing it. Walk the rendered tree and, for each text
  or interactive node, compare `getBBox()` against the boxes of every *later*
  sibling with a non-`none` fill; flag anything covered past a threshold. This is
  a few dozen lines and catches the whole class at once.
- Treat "covered" as a rendering bug even when the element is decorative — it is
  the same defect that will one day land on something load-bearing.
