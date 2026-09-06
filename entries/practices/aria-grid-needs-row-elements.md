---
title: A role=grid whose cells are not inside row elements is dropped from the accessibility tree
tags: [accessibility, aria, css, frontend]
added: 2026-09-06
sources:
  - https://www.w3.org/TR/wai-aria-1.2/#grid
  - https://developer.mozilla.org/en-US/docs/Web/CSS/display#contents
---

## Fact

`grid` owns `row`, and only a `row` owns `gridcell`, `columnheader` and
`rowheader`. A `gridcell` whose nearest role-bearing ancestor is the grid itself
is invalid, and browsers do not tolerate it — they prune the cells rather than
guess. The container is exposed; everything inside it is gone.

CSS Grid pushes directly into that mistake. Placing cells on the track grid
requires them to be children of the grid container, so the obvious markup is one
flat list of cells with no rows in it. `display: contents` on real row elements
resolves the conflict: the row boxes are removed from layout, so their children
become the grid container's items, while the row roles remain in the tree.

## Why it matters

Nothing reports it. The grid looks right, the keyboard handlers work, and the
DOM holds every `aria-label` you set — `document.querySelectorAll('[role=gridcell]')`
finds all of them. Only the accessibility tree is empty, so a screen reader
announces nothing inside the widget.

For an agent it fails misleadingly: tooling that queries by role and name returns
no matches, which reads as "the labels were never applied" and sends you to
re-check the attributes that are, in fact, already correct.

## How to apply

- Keep the chain intact: `grid` → `row` → `gridcell` / `columnheader` /
  `rowheader`, with `.row { display: contents; }` so layout is unaffected.
- Verify against the accessibility tree, not the DOM. A `querySelector` for the
  role succeeds in both the broken and the fixed case, so it proves nothing.
- The same ownership requirement governs `table` → `rowgroup` → `row` → `cell`
  and `treegrid`; a flat `listbox` of `option`s is the exception, not the model.
- Give the rows explicit roles rather than relying on native elements under
  `display: contents`, whose semantics were stripped by older engines.
