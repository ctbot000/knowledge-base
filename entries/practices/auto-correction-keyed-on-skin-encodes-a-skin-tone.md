---
title: An auto-correction whose target is measured on skin has a skin tone baked into it
tags: [image-processing, camera, accessibility]
added: 2026-09-21
sources:
  - https://www.itu.int/rec/R-REC-BT.601
---

## Fact

Face detection makes it easy to meter on the subject instead of the scene, and
the obvious next step — "drive exposure until the face sits at luma 0.55" — is
a constant that only one complexion satisfies. Measured over cheek and nose in
Rec.601 luma, ordinary skin under the same light spans roughly:

```
very light   0.78      medium   0.63      deep   0.33
```

A single target therefore *is* a target skin tone: it lifts dark faces and
pulls down pale ones, and does so most confidently when detection is working
best. The same holds for white balance keyed on skin. Skin is red-leaning by
construction, so `mean(Cr) − mean(Cb)` runs about `0.21…0.31` across
complexions while a genuinely neutral grey card sits near `0`; a "neutral skin"
target reads a warm complexion as a warm lamp and desaturates the person.

## Why it matters

Nothing looks broken. The correction is smooth, the code has no branch on
anything sensitive, and on the developer's own face it is visibly right — which
is how this ships. A consistently mis-exposed preview then reads as a bad
camera rather than as a bad constant.

## How to apply

- Split the measurements by what they are a property of. Exposure, dynamic
  range, clipping and colour cast belong to the *light*: measure them over the
  whole frame. Only quantities that describe **variation** — texture energy,
  chroma *spread*, local contrast — are safe to measure on skin, because they
  say the same thing about any skin.
- Where a skin-referred correction is genuinely wanted, act on the *excess*
  outside a deadband wider than the spread of complexions, so the common case
  is no correction at all.
- Prefer clipping to level as a tone-independent signal.
- Test it directly. Shift the skin statistics across a wide tonal range and
  assert the exposure, contrast and colour outputs are *identical*; that is a
  property the implementation either has or does not.
