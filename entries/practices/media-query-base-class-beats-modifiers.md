---
title: Restyling a base class in a later media query also beats its modifier classes there
tags: [css, cascade, responsive]
added: 2026-10-02
sources:
  - https://www.w3.org/TR/css-cascade-4/#cascade-sort
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity
---

## Fact

A modifier such as `.btn-lg` beats its base `.btn` only because it comes later
in the file, since both are a single class. A media query adds no specificity,
so a `.btn { width: 40px }` inside a breakpoint further down wins again, over
every modifier declared before it, on exactly the screens that query matches.
For the properties the base rule sets, a modifier's declarations placed above
it in the same block are dead too.

## Why it matters

The modifier works on large screens and silently stops working on small ones.
The custom property it sizes from (`width: var(--big)`) still holds the
intended value, so everything else computed from that property, such as
offsets, spacing or a neighbour placed past it, is off by the difference. The
modifier's rule is intact and only shows as overridden in devtools, so the
search starts in the arithmetic, which is correct.

## How to apply

- In a breakpoint that restyles a base class, restate the modifiers after it in
  the same block. Better: have the base read a custom property
  (`width: var(--size)`) that modifiers and breakpoints set, instead of each
  rule setting `width` itself.
- Or raise the modifier to `.btn.btn-lg`, so that it outranks the base
  everywhere.
- Check the computed size of a modified element at each breakpoint, not only
  the property it is meant to follow.
