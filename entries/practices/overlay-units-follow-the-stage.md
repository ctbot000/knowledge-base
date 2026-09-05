---
title: An overlay on a letterboxed stage must size in container units, not viewport units
tags: [css, layout, responsive, frontend]
added: 2026-09-05
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
---

## Fact

A fixed-aspect stage — a canvas game, a video player, an embedded diagram —
letterboxes inside the viewport, so its size and the viewport's size stop
agreeing as soon as the aspect ratios differ.

Overlay chrome sized in `vw`/`vh` therefore scales against the wrong box. A
16:10 stage on a portrait phone occupies a strip a quarter of the viewport's
height; `clamp(11px, 1.5vw, 14px)` resolves against the full 390px width, lands
at its 11px floor, and that floor is enormous next to a 244px-tall stage. The
controls swallow the content, and every `clamp()` bound has to be re-guessed per
breakpoint.

`container-type: size` on the stage makes `cqw`/`cqh` resolve against the stage
itself, so the overlay keeps its proportions at every viewport shape.

## Why it matters

It fails in exactly the configuration that is hardest to notice: the developer's
landscape window is close enough to the stage's own aspect ratio that viewport
units look right, and the layout only collapses where the letterboxing is
severe. The symptom — a HUD that covers the game — reads as a padding bug rather
than a units bug, so it gets patched breakpoint by breakpoint instead of fixed.

## How to apply

- Put `container-type: size` on the letterboxed element, then size its overlay
  in `cqh`/`cqw`: `font-size: clamp(9px, 3.2cqh, 14px)`.
- The container needs a definite size from its own ancestors — `container-type:
  size` applies `contain: size`, so the element must not be sized by its
  contents.
- Keep the `clamp()` floor and ceiling for legibility; the container unit is
  what carries the scaling between them.
- Media queries still read the viewport, which is what you want for decisions
  about the device rather than about the box — an "turn your phone sideways"
  notice belongs in `@media (orientation: portrait) and (pointer: coarse)`.
