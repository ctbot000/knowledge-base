---
title: A filter radius fixed in pixels is calibrated to one subject size, not to the image
tags: [graphics, image-processing, computer-vision]
added: 2026-09-20
---

## Fact

Any spatial filter tuned in pixels — a smoothing blur, a high-pass, an unsharp
mask, a morphological open — is implicitly tuned to one size of subject. When
the subject's size in frame varies, the same radius means a different thing at
every distance.

A face fills 40% of the frame width at arm's length and 12% across a room: a
radius that softens pores at the near scale erases the whole face at the far
one. The fix is to key the radius to a feature the detector already measures,
not to the frame:

```js
radius = clamp(faceWidth * imageHeight * k, lo, hi) * userSlider;
```

The slider then multiplies a derived value instead of being the value.

## Why it matters

The symptom is "this setting is wrong", not "this setting is scale-dependent",
so it gets retuned against whatever the subject happened to be doing during
testing — which bakes that one distance into the defaults. Every later report
disagrees with every other, because each reporter sat at a different distance.

It is the same failure whenever scale is free: a document scanned at another
DPI, a map at another zoom level, a render at another output size.

## How to apply

- Derive the radius from a measured feature; the detector that finds the
  subject almost always hands you one for free.
- Clamp the derived value at both ends, so a bogus measurement — a detection on
  a reflection, a zero-size box — cannot explode or collapse the filter.
- Keep the user's control as a multiplier on the derived radius.
- Verify by asserting the derived radius scales: two subject sizes in, two
  proportional radii out, both inside the clamp.

Related: [[radial-kernel-on-a-non-square-grid]],
[[palette-is-calibrated-to-its-shading-model]].
