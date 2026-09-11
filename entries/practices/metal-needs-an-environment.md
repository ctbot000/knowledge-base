---
title: A metal surface lit only by punctual lights is black everywhere except its highlight
tags: [graphics, rendering, pbr]
added: 2026-09-11
---

## Fact

In a physically based shading model a metal has no diffuse term: its colour is
entirely the specular reflection of whatever radiance arrives at it. Point,
spot and directional lights are *punctual* — they deliver energy from a single
direction — so they can only produce a narrow highlight where the mirror
direction happens to line up with the viewer. Everywhere else a metal has
nothing to reflect, and nothing is what it shows.

Measured on one chrome object at `metalness: 1.0, roughness: 0.3`, lit by a
single directional light and no environment, three sample points read
`(63,33,13)`, `(12,8,4)` and `(0,0,0)` — mean 15/255. Adding an image-based
environment and changing nothing else took the same points to `(102,53,23)`,
`(72,48,28)` and `(26,6,1)`, mean 40. The literal black pixel is the ordinary
case, not an edge one.

## Why it matters

The failure looks like a lighting problem, so the response is to add lights or
turn them up — which cannot work, because more punctual light only brightens the
highlight that is already the one lit part. Time then goes into the light rig,
the tone mapper and the exposure, none of which is the missing term.

It is most common when porting art from a renderer that had no notion of
metalness, where "shiny metal" was a colour and a specular power, and the same
material description now means something entirely different.

## How to apply

- Give the scene an environment before tuning any light. A 64×32 canvas gradient
  run through a prefilter is enough to make metal read as metal; it does not need
  to be a captured HDRI.
- Sample the darkest metal away from its highlight to check the fix. The
  highlight looks correct under every wrong setting.
- If metal must stay black for a reason, lower `metalness` instead — a partly
  dielectric material keeps a diffuse term that punctual lights can reach.
- Roughness does not rescue it: a rougher metal spreads the same missing energy
  over a wider lobe, so it gets dimmer, not fuller.

Related: [[palette-is-calibrated-to-its-shading-model]],
[[lamp-power-cannot-widen-the-pool]].
