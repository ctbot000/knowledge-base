---
title: Redefining grid-template-areas re-points the existing track list at different areas
tags: [css, grid, layout, responsive]
added: 2026-09-12
sources:
  - https://drafts.csswg.org/css-grid/#explicit-grid
---

## Fact

`grid-template-rows` is a positional list of sizes and `grid-template-areas`
decides which area sits on which track. Changing only the areas — the usual move
inside a media query — hands every size to a different area, silently.

```css
.app { grid-template-rows: auto minmax(0, 1fr);
       grid-template-areas: "top top" "room tray"; }

@media (max-width: 900px) {
  .app { grid-template-areas: "top" "room" "tray"; }  /* rows left behind */
}
```

`tray` shared row 2 with `room`; now it is row 3. The areas declare more rows
than the track list sizes, so row 3 is created implicitly and sized by
`grid-auto-rows` — `auto` by default. The `1fr` stays on row 2, and `room`
absorbs every spare pixel in the container.

## Why it matters

Nothing errors and the wide layout is untouched, so the regression exists at one
breakpoint only. It presents as a section floating in a large empty band with
the section below it squeezed — which reads as a centring or padding bug in the
child, not a track-sizing bug in the parent. Devtools shows the *computed* track
list with the extra row already resolved, so it agrees with the picture rather
than with the declaration.

## How to apply

- Restate `grid-template-rows` (and `-columns`) in the same rule that restates
  `grid-template-areas`. They are one declaration and must move together.
- Compare counts, not appearances: `getComputedStyle(el).gridTemplateRows`
  returns one entry per row, so more entries than the areas declare is the bug.
- `grid-auto-rows` really does size that leftover row, so setting it explicitly
  turns a silent `auto` into something you chose.
