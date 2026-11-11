---
title: three.js Color.setHSL and setRGB take their numbers in the linear working colour space, unlike hex values and CSS strings
tags: [three.js, graphics, colour]
added: 2026-11-12
sources:
  - https://threejs.org/docs/#api/en/math/Color
  - https://github.com/mrdoob/three.js/blob/dev/src/math/Color.js
---

## Fact

With colour management on (the default since r152), a `Color` made from a hex
number or a CSS string is read as sRGB and converted to the working space,
linear sRGB: `setHex` and `setStyle` default their `colorSpace` argument to
`SRGBColorSpace`. `setHSL(h, s, l)` and `setRGB(r, g, b)` default it to
`ColorManagement.workingColorSpace` instead, so their numbers are stored as
they are, as linear values. `getHSL` and `getRGB` default the same way.
Checked on r186.

## Why it matters

A colour computed at run time comes out with the right hue and the wrong
tone. `setHSL(0.33, 0.6, 0.46)` is meant as a mid green; taken as linear, a
lightness of 0.46 displays at about 0.71, so the surface is pale and washed
out beside materials built from hex strings. Nothing errors, and the hue is
right, so it reads as a lighting or material problem. It shows up wherever a
colour is animated or generated: hue cycling, per-instance tints, palettes
from a seed.

## How to apply

Say which space the numbers are in:

```js
material.color.setHSL(hue, 0.6, 0.46, THREE.SRGBColorSpace);
material.color.setRGB(0.3, 0.75, 0.29, THREE.SRGBColorSpace);
color.getHSL(target, THREE.SRGBColorSpace); // to compare with design values
```

`offsetHSL` has no such argument: it reads and writes in the working space,
so do the read, the change and the write yourself when the offsets are meant
in sRGB.
