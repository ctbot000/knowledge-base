---
title: An oversized item in an auto grid track is not centred, because the track grew to fit it
tags: [css, grid, layout]
added: 2026-09-22
sources:
  - https://www.w3.org/TR/css-grid-1/#auto-tracks
  - https://www.w3.org/TR/css-align-3/#overflow-values
---

## Fact

`place-items: center` centres an item inside its **track**, not inside the grid
container. An `auto` track is `minmax(auto, max-content)`, so a single item
wider than the container makes the track as wide as the item — and centring a
900px item in a 900px track moves it nowhere. The track starts at the content
edge, so the item ends up flush left and overflowing only to the right.

A 900px child in a 300px box, measured in Chromium, as the offset between the
child's centre and the container's:

| parent | offset |
| --- | --- |
| `display: grid; place-items: center` | **300px** |
| `grid-template-columns: minmax(0, 1fr)` | 0 |
| `grid-template-columns: 100%` | 0 |
| `display: flex; justify-content: center` (item `flex: none`) | 0 |

Flex gets it right: alignment there is against the line box, which is the
container. Only grid has a track in between that can grow.

## Why it matters

The failure is asymmetric, which points away from the cause: the element sits
visibly *off to one side* rather than overflowing evenly, so it reads as a wrong
`left`, a stray transform or a margin, while the `place-items: center` at fault
looks like the one line that must be right. It also appears only once the item
outgrows the container, so it survives every wide-viewport check and lands on
phones.

## How to apply

- Cap the track — `minmax(0, 1fr)`, `minmax(0, auto)` or `100%` — whenever a
  grid cell holds something that can be wider than the container: a canvas, a
  scaled board, a wide table, a long unbroken string.
- Reach for flex when the only job is to centre one oversized child.
- Verify by measuring the two centres, not by reading the alignment rules.

Related: [[auto-grid-track-blocks-flex-shrink]] — the same auto track, the same
fix, seen from its minimum instead of its maximum.
