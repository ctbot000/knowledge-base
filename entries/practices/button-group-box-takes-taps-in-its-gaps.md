---
title: A group of buttons takes taps anywhere in its box, gaps and empty cells included, so it can cover a neighbour no button of it overlaps
tags: [css, dom, pointer-events, testing]
added: 2026-10-02
sources:
  - https://drafts.csswg.org/cssom-view/#dom-document-elementfrompoint
  - https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events
---

## Fact

Hit testing uses an element's whole border box, whether or not anything is
painted there. A flex or grid container of controls that takes pointer events
(the default) receives a tap in its gaps, in an empty grid cell, or in the
slack left where an item is aligned to one end of its area. Where two such
groups overlap, the one painted later (later in the document, at the same
stacking level) takes those taps, though none of its controls is drawn there.

## Why it matters

The covered control fails on part of its face only: a tap on its edge does
nothing, while its middle works. A layout test that compares the controls'
own rects for overlap passes, since no two controls meet; only the boxes of
their groups do. A typical case is a corner cluster with one tall button
spanning two rows (`align-items: end` leaves an empty cell above it), and a
column of buttons beside it that reaches down into that cell.

## How to apply

- In overlap sweeps, compare the boxes of the groups that take taps, not only
  their buttons; or hit-test the edges of each control with
  `elementFromPoint`, which returns the group's container where it wins.
- In an overlay HUD, give each group `pointer-events: none` and its controls
  `pointer-events: auto`: only what is drawn takes a tap, and the rest passes
  through to the scene below. A hit test then skips the group, see
  [[element-from-point-skips-tap-through-layers]].
