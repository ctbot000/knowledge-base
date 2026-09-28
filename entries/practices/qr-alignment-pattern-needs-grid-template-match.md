---
title: A QR alignment pattern searched as 1:1:1 runs along image rows is missed on rotated codes
tags: [computer-vision, image-processing, qr-code]
added: 2026-09-28
sources:
  - https://github.com/zxing/zxing/blob/master/core/src/main/java/com/google/zxing/qrcode/detector/AlignmentPatternFinder.java
---

## Fact

ZXing-style detectors look for the alignment pattern by scanning image rows for
light-dark-light runs, each within half a module of the estimated module size.
A row crosses a rotated pattern's rings diagonally, which stretches every run
by up to √2 at 45°. Add a little blur and the real pattern fails the test, while
a chance 1:1:1 run in the data area passes and is used for the perspective
transform.

Matching the whole 5×5 template (dark ring, light ring, dark centre), sampled at
steps of the symbol's own module vectors, does not depend on rotation or skew.

## Why it matters

The alignment pattern is the fourth point of the perspective fit. Losing it, or
locking onto a look-alike a few modules away, makes every tilted code
undecodable. The finder patterns are all found, so it looks like a sampling or
error-correction bug.

## How to apply

- Take the module vectors from the three finder centres (or from the current
  homography), then slide the template over a window around the predicted
  centre. Score by mismatches, and take the centroid of the lowest plateau.
- Keep a few candidates and confirm each by a full decode, because
  Reed-Solomon is the only reliable judge of a fit.
- On large versions, find the alignment patterns nearest the finders first and
  refit a least-squares homography after each, so every prediction is a short
  extrapolation.
