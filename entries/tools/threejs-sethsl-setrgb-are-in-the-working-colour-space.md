---
title: A three.js Color's own numbers (setRGB, setHSL, .r .g .b) are linear, unlike its hex values and CSS strings
tags: [three.js, graphics, colour]
added: 2026-11-12
updated: 2026-11-22
sources:
  - https://threejs.org/docs/#api/en/math/Color
  - https://github.com/mrdoob/three.js/blob/dev/src/math/Color.js
---

## Fact

With colour management on (the default since r152), a `Color` made from a hex
number or a CSS string is read as sRGB and converted to the working space,
linear sRGB: `setHex` and `setStyle` default their `colorSpace` argument to
`SRGBColorSpace`. `setHSL(h, s, l)` and `setRGB(r, g, b)` default it to
`ColorManagement.workingColorSpace`, so their numbers are stored as they are;
`getHSL` and `getRGB` default the same way, and the `.r`, `.g`, `.b` fields
always hold the linear values. Checked on r186.

## Why it matters

Numbers meant as sRGB go wrong both ways, silently. Written: `setHSL(0.33,
0.6, 0.46)`, meant as a mid green, displays at a lightness of about 0.71,
pale and washed out beside hex-built materials. Read: a test on `.r` written
from hex codes misfires, since `#f3f6fb` holds r = 0.896, so `c.r > 0.9`
("near white") is false; code that recolours parts by their colour skips
them, and nothing errors.

## How to apply

Say which space the numbers are in:

```js
material.color.setHSL(hue, 0.6, 0.46, THREE.SRGBColorSpace);
material.color.setRGB(0.3, 0.75, 0.29, THREE.SRGBColorSpace);
color.getRGB(target, THREE.SRGBColorSpace); // to compare with design values
color.getHexString() === 'f3f6fb';          // hex getters convert back to sRGB
```

To swap a shared, cached material, match the material object itself rather
than its colour. `offsetHSL` has no colour space argument: it works in the
working space, so do the read, change and write yourself when the offsets
are meant in sRGB.
