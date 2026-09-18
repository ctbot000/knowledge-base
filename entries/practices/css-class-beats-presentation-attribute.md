---
title: A CSS class that sets fill or stroke silently wins over setAttribute
tags: [svg, css, frontend]
added: 2026-09-19
sources:
  - https://www.w3.org/TR/SVG2/styling.html#PresentationAttributes
---

## Fact

SVG presentation attributes — `fill`, `stroke`, `opacity`, `stroke-width` and
the rest — are not ordinary attributes. They are folded into the cascade as if
they were author declarations of *zero* specificity, below every real rule.

So `node.setAttribute('fill', colour)` has no visible effect on an element whose
class already declares a `fill`. The attribute is set, `getAttribute` reads it
back, the DOM inspector shows it, and the element keeps painting the class
colour. Nothing warns.

The same element responds immediately to `node.style.fill = colour`, because an
inline style outranks the class.

## Why it matters

It is the natural way to write a data-driven drawing: style the static look in
a stylesheet, then set the one changing colour from script. Half of that works.
An element whose class happens not to mention `fill` updates correctly, and its
neighbour whose class does mention it never changes — so the bug looks like a
broken colour calculation, or like only some elements being reached, rather
than a cascade problem. Both elements are usually written by the same loop.

It bites hardest when a class is added later, for theming or a shared look:
code that worked for months stops updating the moment a rule sets that property.

## How to apply

- Set anything script-controlled through `style`, not `setAttribute`:
  `node.style.fill = colour`, `node.style.strokeWidth = w`.
- Or keep the property out of CSS entirely for elements script will drive, and
  let the presentation attribute own it.
- Do not mix the two on one property. Pick per property, per element class.
- The fixed direction is worth remembering: presentation attribute < any CSS
  rule < inline style < `!important`.
