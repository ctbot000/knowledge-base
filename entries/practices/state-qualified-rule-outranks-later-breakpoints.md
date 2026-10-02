---
title: A state-qualified rule in one breakpoint outranks the plain rule in every later breakpoint, in that state only
tags: [css, cascade, responsive]
added: 2026-10-02
sources:
  - https://www.w3.org/TR/selectors-4/#specificity-rules
  - https://developer.mozilla.org/en-US/docs/Web/CSS/:where
---

## Fact

A media query adds no specificity, so a later breakpoint overrides an earlier
one only when their selectors tie, by source order. An override qualified by a
page state, such as `body:not(.touch) .chat` or `html.dark .chat`, scores more
than `.chat` (`:not()` counts as its argument), so placed in one breakpoint it
beats the plain `.chat` rules of every later breakpoint wherever both match.
`:where()` counts for nothing: `:where(body:not(.touch)) .chat` ties `.chat`,
so it beats a `.chat` rule above it and loses to the ones below, by order.

## Why it matters

The later breakpoints keep working in the other state, so the bug shows only
in one state (mouse devices, say) and only at sizes where two breakpoints
overlap, while the rule that loses looks correct in the file. The usual patch
is `!important` in each later breakpoint, which the next override then has to
beat in turn.

## How to apply

- Wrap the state qualifier in `:where()` when the override must not outrank
  rules further down: `:where(body:not(.touch)) .chat`. Supported since
  Chrome 88, Firefox 78 and Safari 14.
- `!important` on a later breakpoint's plain rule for the same element is a
  sign that an earlier qualified rule already outranks it.
- Check the computed value at each breakpoint in both states, not only in the
  state the override was written for.

Related: [[media-query-base-class-beats-modifiers]] (the same tie, broken by
order), [[theme-scoped-selector-outranks-component-class]].
