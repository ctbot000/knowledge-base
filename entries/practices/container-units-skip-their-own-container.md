---
title: Container query units resolve against an ancestor container, never the element's own
tags: [css, layout, container-queries]
added: 2026-09-14
sources:
  - https://drafts.csswg.org/css-contain-3/#container-lengths
---

## Fact

`cqw`, `cqh`, `cqi` and `cqb` measure the nearest **ancestor** container. An
element that declares `container-type` does not become its own query container,
because the answer would feed back into the size it was measured from.

So a container unit written in a rule that targets the container itself measures
something else entirely — the next container up, or, if there is none, the small
viewport:

```css
.stage {
  container-type: size;   /* 1008px wide here */
  perspective: 120cqw;    /* resolved against the 1366px viewport */
}
```

The same declaration one element down is correct, which is what makes it hard to
see: `.stage > .camera { perspective: 120cqw }` measures the stage.

## Why it matters

Nothing errors and nothing is obviously broken. The property takes a plausible
value that is wrong by whatever ratio the two boxes happen to have — 36% in the
case above — so the symptom is a design that looks subtly off (a flat-looking
perspective, padding that breathes wrong at one breakpoint) rather than a unit
bug. It is invisible whenever the element and the outer container are close in
size, which is most of the time during development.

Custom properties make it worse, because a `cq` length in a custom property is
resolved **where it is used**, not where it is declared. One `--room: 140cqw` on
the container can mean one length in the container's own rules and a different
one in every descendant that reads it — half the geometry right, half wrong.

## How to apply

- Never write `cq*` in a declaration on the element carrying `container-type`.
  Put those properties on a child wrapper that exists for the purpose.
- Read a computed value back when a container unit drives geometry:
  `getComputedStyle(el).perspective` against the container's own
  `getBoundingClientRect().width` says immediately which box won.
- For "a fraction of this element's own size", prefer `%` where the property
  accepts it; `perspective`, `translateZ` and `box-shadow` offsets do not, so
  those are the ones that need the wrapper.
- Sizing a descendant against the container is the normal, correct use — see
  [[overlay-units-follow-the-stage]].
