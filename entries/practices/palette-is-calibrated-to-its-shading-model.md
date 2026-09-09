---
title: A colour palette is calibrated to its shading model, not to the screen
tags: [graphics, color, rendering]
added: 2026-09-09
---

## Fact

Colours chosen against flat fills are final values: what is written is what is
seen. The moment the same colours are fed through a lit renderer they become
albedo, and every stage multiplies them down — ambient term, `N·L`, distance
attenuation, fog. A mid-dark `#2c2b3a` that read as "moody slate" flat can leave
the screen at a few percent brightness once shaded.

The loss is multiplicative and compounds, so the darkest entries in a palette
disappear entirely while the lightest merely dim. The palette does not scale
uniformly; it collapses from one end.

## Why it matters

Changing renderer is normally treated as a rendering task, with the art assumed
portable. It is not, and the result looks like a lighting bug rather than a
colour one — which sends the work into the light rig, where turning everything
up only blows out whatever was already bright.

The same trap catches a flat design system moved under a translucent or blended
surface, and any palette moved from sRGB fills into a linear-space pipeline.

## How to apply

- Re-pick albedo against the new pipeline rather than scaling the old values.
  Expect to lift the dark end substantially and the light end barely.
- Sanity-check the worst case first: darkest material, minimum ambient, maximum
  fog distance. If that reads, the rest will.
- Keep the two palettes as separate data if both renderers survive. One shared
  table tuned for neither is worse than two tuned tables.
