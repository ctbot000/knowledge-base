---
title: A responsive flex-direction flip turns every item's flex-basis from a width into a height
tags: [css, flexbox, layout, responsive]
added: 2026-09-18
sources:
  - https://www.w3.org/TR/css-flexbox-1/#flex-basis-property
  - https://developer.mozilla.org/en-US/docs/Web/CSS/flex-basis
---

## Fact

`flex-basis` sizes the **main axis**, whichever axis that currently is. The
shorthand `flex: 1 1 150px` therefore means "150px wide" in a row container and
"150px tall" in a column one — the declaration on the item does not change, the
container's `flex-direction` does.

Measured with one line of text in each item, in a 300px container:

```css
.item { flex: 1 1 150px; }
```

| container | rendered |
| --- | --- |
| `flex-direction: row` | 150 x 26 |
| `flex-direction: column` | 300 x 150 |

The item grew to 150px of height from nothing but a basis meant as a width.

## Why it matters

The pattern that triggers it is the most ordinary responsive rule there is:
`flex: 1 1 <width>` on cards in a row, then `flex-direction: column` inside a
media query to stack them. The desktop layout is correct, and on a phone every
card becomes a fixed-height box with its content stranded at the top and a
column of dead space below.

It does not read as a sizing bug, because nothing overflows and nothing is
cut off — it reads as bad spacing, so the fix people reach for is padding or
`gap`, neither of which touches the cause. It also survives review: the rule
that breaks it is in a media query, several hundred lines from the `flex`
declaration it silently reinterprets.

## How to apply

- In the media query that flips the direction, reset the basis too:
  `flex: 0 0 auto; width: 100%`.
- Prefer `width` over `flex-basis` for a fixed preferred size, so the value is
  bound to an axis by name and the flip cannot re-aim it
  ([[flex-basis-does-not-size-an-auto-container]] is the other half of that
  advice).
- Verify by measuring `getBoundingClientRect().height` at the narrow breakpoint;
  an over-tall card looks like a padding choice in a screenshot.
