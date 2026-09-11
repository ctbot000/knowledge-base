---
title: A grouping property silently turns transform-style preserve-3d into flat
tags: [css, 3d, transforms, frontend]
added: 2026-09-11
sources:
  - https://drafts.csswg.org/css-transforms-2/#grouping-property-values
  - https://developer.mozilla.org/en-US/docs/Web/CSS/transform-style
---

## Fact

`opacity` below 1, any `filter`, `mask`, `clip-path`, `overflow` other than
`visible`, and `will-change` of those are *grouping properties*: the element
must be rendered into a single plane first, so the **used** value of its
`transform-style` becomes `flat` no matter what the stylesheet says. Its 3D
children collapse into the parent's plane.

The collapse is total, not subtle. In a scene tilted 60°, a child plane standing
upright out of the floor measured 35×53 px on screen; adding `opacity: .99` to
its parent — or a no-op `filter: brightness(1.001)` — took it to 35×**0**,
because upright is edge-on once everything is squashed into the floor.

`getComputedStyle` keeps reporting `preserve-3d` throughout. The computed value
never changed; only the used value did.

## Why it matters

The obvious way to animate a 3D object away is to fade it, and the flattening
starts at the first frame under `opacity: 1` — so the object snaps flat exactly
when the transition begins, which reads as "my transform is wrong", not "my
opacity is wrong".

It arrives from directions that do not look like styling decisions either: a UA
stylesheet putting `overflow: clip` on a `<button>` used as a 3D container, a
`filter: drop-shadow` added for polish, a `clip-path` cutting a silhouette.
Every debugging tool agrees with the author, because the declared value is
intact.

## How to apply

- Fade the leaves, not the group: put `opacity`/`filter` on elements that have no
  3D children of their own, and leave the container alone.
- Set `overflow: visible` explicitly on any element you give `preserve-3d`,
  especially form controls, where the UA sheet may clip.
- A grouping property is fine *outside* the 3D context — wrap the scene in a
  plain parent and fade that instead.
- Detect it by measuring, not by reading style: `getBoundingClientRect()` on an
  upright child drops to roughly zero height when the subtree has flattened.
