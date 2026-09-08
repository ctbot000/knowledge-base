---
title: A flex item that grows ignores aspect-ratio, because both of its axes are then definite
tags: [css, flexbox, layout]
added: 2026-09-08
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio
---

## Fact

`aspect-ratio` only sizes an axis that is still `auto`. Give an element a
definite width *and* a definite height and the property is inert — it is not
overridden, it never applies.

A flex item reaches that state without anything in its own rule saying so. In a
column flex container, `flex-grow` resolves the item's main size from the free
space, and the default `align-items: stretch` resolves its cross size from the
line. Both axes are now definite, and the declared ratio does nothing:

```css
.stage { aspect-ratio: 1200 / 760; flex: 1 1 auto; }   /* renders 1.24 */
.stage { aspect-ratio: 1200 / 760; flex: 0 0 auto; }   /* renders 1.58 */
```

Measured in a 400x900 column container, the growing item comes out 400x323 and
the non-growing one 400x253. Adding an explicit `width` changes nothing; the
grow is what does it.

## Why it matters

The symptom is a stretched picture, not a broken layout, so it is read as a
renderer bug. A canvas or video stretched by a distorting factor looks like bad
drawing code, and the CSS declaring the ratio is right there in the rule,
apparently being honoured on the axis you happen to check.

It hides on a desktop window whose shape is already close to the ratio, and
appears at the shapes furthest from it — a landscape stage on a portrait phone.

## How to apply

- Take the item out of the flex sizing: `flex: 0 0 auto`, and centre it with a
  wrapper (`display: grid; place-items: center`) that grows in its place.
- There is no robust pure-CSS form of "fit a fixed ratio inside a box bounded on
  both axes". When both bounds are real, compute the size in script from the
  measured wrapper — floor the measurement, since a hidden surface reports zero
  ([[zero-measurement-poisons-derived-layout]]).
- Verify by measuring the rendered ratio, not by reading the rule.

Related: [[svg-intrinsic-size-beats-the-box]], [[overlay-units-follow-the-stage]].
