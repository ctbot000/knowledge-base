---
title: Blockification applies to a flex or grid item, not to anything inside it
tags: [css, layout, flexbox]
added: 2026-09-07
sources:
  - https://drafts.csswg.org/css-display/#blockify
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_display/display
---

## Fact

A flex or grid container blockifies its **direct children**: an inline element
used as an item computes to `display: block`, so a `<button>` or `<span>` laid
out as a grid item reports a real box without anyone setting `display` on it.

That conversion stops there. The item's own descendants keep whatever display
they had, so an inline wrapper one level down is still inline — and `width` and
`height` do not apply to inline boxes. A `<span>` written as the fill-the-parent
wrapper measures `0 × 0` despite `width: 100%; height: 100%`.

Anything the wrapper contains collapses with it. `position: absolute; inset: 0`
children resolve against a zero-sized containing block, so they are zero too.

## Why it matters

Every element an author would think to inspect measures correctly: the container
is right, the item is right, and the computed styles on the wrapper say `100%`.
Only `getBoundingClientRect()` on the wrapper itself reveals the collapse.

Nothing errors and nothing paints, so the symptom gets attributed to whatever
exotic feature the wrapper was there to carry — a 3D transform, `preserve-3d`,
`backface-visibility`, a clip path — rather than to `display`.

## How to apply

- Give any wrapper expected to fill its item an explicit `display: block`
  (or `grid`/`flex`). Do not rely on inheriting the item's blockification.
- When a child of a flex or grid item does not paint, measure the child's own
  box before investigating transforms; a `0 × 0` rect is this bug.
- `div` wrappers hide the problem by default and `span` wrappers expose it,
  which is why the same structure works in one component and not another.
