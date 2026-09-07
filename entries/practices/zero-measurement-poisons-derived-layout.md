---
title: A layout measured while the surface is hidden is zero, and rescaling from it cannot recover
tags: [css, layout, canvas, frontend]
added: 2026-09-07
updated: 2026-09-08
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect
---

## Fact

`getBoundingClientRect()` on an element inside a hidden or collapsed surface
returns zeros — a background pane, a `display:none` ancestor, an embedded view
that is not currently shown. The read succeeds; it is the box that is empty.

Anything derived from that measurement inherits the collapse. A canvas scene
that sizes its world from the container gets sub-pixel cells, and every object
placed in that world is stored at a coordinate that carries no information. When
the surface reappears, the usual remedy — rescale the stored coordinates by the
ratio of new size to old — cannot help: it multiplies noise by a large number.

## Why it matters

The visible symptom appears long after the cause, in a surface that is now fully
laid out, so it reads as a broken renderer rather than a stale measurement.
Positions come back bunched into a band, or piled in one corner, and the code
that produced them is correct for the size it was given.

It also hides in exactly the place work gets verified: a developer's window is
always visible, while automated runs, backgrounded tabs and hidden panes are
where the zero arrives.

## How to apply

- Clamp the measurement to a usable floor rather than trusting it:
  `width = Math.max(MIN, Math.round(rect.width))`. A small sane world is
  recoverable by rescaling; a zero-sized one is not.
- Regenerate rather than rescale whenever the state is still disposable — before
  the user has interacted, a fresh layout fits the new shape far better than a
  stretched old one. Rescaling is for state that must be preserved.
- Store positions in units that survive a re-layout — grid cells, fractions of a
  container — so a resize changes only the conversion to pixels.
- The collapse reaches CSS too: in such a surface the viewport itself reports 0,
  so every `vw`/`vh`-derived custom property resolves to zero and any size built
  on it — font sizes included — disappears. Floor the token itself:
  `--size: max(11rem, min(20rem, 78vw))`.
- Recover automatically rather than measuring once: a `ResizeObserver` on the
  element fires as soon as it has a real box, which is the moment the surface
  becomes visible.
