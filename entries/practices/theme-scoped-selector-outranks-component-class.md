---
title: A theme-scoped element selector outranks a component's own class
tags: [css, theming, frontend]
added: 2026-09-19
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity
---

## Fact

Scoping a rule to a theme adds specificity to it. `:root[data-theme="light"] a`
scores (0,2,1) — one pseudo-class, one attribute, one element — which beats a
two-class component rule such as `.btn.primary` at (0,2,0). The theme rule wins
even though it names only a bare element.

So a link styled as a button loses its own colour the moment a theme override
for `a` exists. When the component sets a background from the same variable the
theme assigns to link text, the label is painted the exact colour of the button
underneath it.

## Why it matters

Nothing errors and nothing is missing: the element is in the DOM, the text is in
the element, and the computed style is a real colour. The control simply reads
as an empty rectangle, and only in the theme whose override applies — so it
survives any check run in the other theme.

The same trap catches any global element rule given a scope: a
`[dir="rtl"] a`, a `.dark button`, a `:root[data-density] input`.

## How to apply

- Match the specificity where it matters rather than reaching for `!important`:
  `a.btn` is (0,1,1) and `a.btn.primary` is (0,2,1), which ties the theme rule
  and wins on order when it comes later in the sheet.
- Keep theme rules on custom properties instead of on painted properties. A
  theme that only redefines `--accent` cannot outrank anything, because every
  component still resolves its own declaration.
- Verify a control by its computed colour against its computed background, not
  by eye in one theme — equal values are the signature of this bug.
