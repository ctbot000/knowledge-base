---
title: A scroll container zeroes its own automatic minimum size, not its parent's
tags: [css, grid, layout]
added: 2026-09-18
sources:
  - https://drafts.csswg.org/css-sizing-3/#automatic-minimum-size
  - https://drafts.csswg.org/css-grid/#min-size-auto
---

## Fact

A grid item has `min-width: auto`, so a `1fr` track — really `minmax(auto, 1fr)`
— can never be narrower than that item's content-based minimum. Wrapping the
oversized thing in `overflow: auto` looks like the fix and is not. A scroll
container's automatic minimum *is* 0, but only for the box carrying the
`overflow`; every ancestor still resolves `auto` from the content inside it.

Measured in a 300px container, with `min-width: 500px` on the innermost box:

| structure | item width |
|---|---|
| grid item → scroller → wide box | **500** — track blown out |
| same, plus `min-width: 0` on the grid item | 300, scroller scrolls |
| grid item *is* the scroller | 300, scroller scrolls |
| column flex item → scroller → wide box | 300 |

The column flex case escapes only because width is then the *cross* size,
resolved by `stretch`. A **row** flex container blows out exactly like grid,
because there width is the main size and `min-width: auto` applies again.

## Why it matters

The symptom is a page that scrolls sideways on a phone, and the element that is
too wide is not the one with the offending rule — it is two levels up, carrying
no width declaration at all. The scroller looks innocent because its
`scrollWidth` is correct; it simply never gets a chance to scroll.

## How to apply

Put `min-width: 0` on the grid item — `.grid > * { min-width: 0 }` is a safe
blanket rule — or make the grid item itself the scroll container. `min-height: 0`
is the same fix in the block axis.
