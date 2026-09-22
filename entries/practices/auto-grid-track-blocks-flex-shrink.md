---
title: A nowrap flex row inside an auto grid track overflows instead of shrinking, and min-width:0 does not help
tags: [css, grid, flexbox, layout]
added: 2026-09-22
sources:
  - https://www.w3.org/TR/css-grid-1/#auto-tracks
  - https://www.w3.org/TR/css-flexbox-1/#intrinsic-sizes
---

## Fact

A grid track written as `auto` is `minmax(auto, max-content)`, and its floor is
the item's min-content contribution. For a `flex-wrap: nowrap` flex container
that contribution is the **sum of its own items' base sizes**, so the track is
sized to the whole un-shrunk row and the row overflows its parent.

`min-width: 0` on the flex items — the usual remedy for a flex item that will
not shrink — does nothing here. Ten items at `flex: 0 1 60px` in a 300px grid,
measured in Chromium:

| parent | track | item |
| --- | --- | --- |
| `display: grid` (auto track) | 600px | 60px |
| `display: grid` (auto track) + `min-width: 0` on items | 600px | 60px |
| `grid-template-columns: minmax(0, 1fr)` | 300px | 30px |
| plain block | 300px | 30px |

The items shrink perfectly well; they are simply never asked to, because the
track grew to fit them first. A plain block parent has no such floor and works.

## Why it matters

The symptom is content running off the side of a container that has an explicit
width, which reads as a missing `overflow` or a wrong width somewhere. Every
rule you inspect — the item's `flex-shrink`, its `min-width`, the parent's
`width` — looks correct, because the deciding value is the track's automatic
minimum and it appears in no declaration.

It also hides on wide viewports, where the row happens to fit, and appears only
once the container is narrower than the row's natural width.

## How to apply

- Write the track as `minmax(0, 1fr)` (or `minmax(0, auto)`) whenever the cell
  holds a `nowrap` flex row, a long text run, or anything with an intrinsic
  size. `1fr` on its own is `minmax(auto, 1fr)` and has the same floor.
- Do not reach for `min-width: 0` on the items first; confirm the parent track
  is capped before touching the items at all.
- Verify by measuring the rendered container width against its parent's, not by
  reading the rules.

Related: [[svg-intrinsic-size-beats-the-box]], [[aspect-ratio-loses-to-flex-grow]].
