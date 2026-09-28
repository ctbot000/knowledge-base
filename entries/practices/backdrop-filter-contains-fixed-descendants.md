---
title: A backdrop-filter makes its element the containing block for position:fixed descendants
tags: [css, layout, frontend]
added: 2026-09-28
sources:
  - https://drafts.fxtf.org/filter-effects-2/#BackdropFilterProperty
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block
---

## Fact

Like `transform` and `filter`, any `backdrop-filter` other than `none` turns
its element into the containing block for `position: fixed` (and absolute)
descendants. A fixed child is then positioned against that element's box, not
the viewport, and scrolls with it.

## Why it matters

The textbook frosted-glass header, `position: sticky` plus a backdrop blur, is
the natural home for navigation. Restyle that navigation as a phone tab bar
with `position: fixed; bottom: 0` and it lands at the bottom edge of the header
instead, at the top of the screen, overlapping the brand. Nothing in the
tab bar's own rules explains it, and `getComputedStyle` still reports
`position: fixed`.

## How to apply

- Check every ancestor for `transform`, `filter`, `backdrop-filter`,
  `perspective`, `contain: layout/paint` and `will-change` on those properties
  when a fixed element is mispositioned.
- Drop the ancestor's `backdrop-filter` in the breakpoint where the child
  becomes fixed (an opaque background is the usual substitute), or move the
  fixed element out of that ancestor in the DOM.
