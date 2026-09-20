---
title: The textbook local image warp folds near its own rim, and worst at small displacements
tags: [graphics, geometry, image-processing]
added: 2026-09-20
sources:
  - https://www.gson.org/thesis/warping-thesis.pdf
---

## Fact

Gustafsson's local translation — the primitive behind every "liquify" brush and
face-slimming filter — maps a pixel back with

```
u = x - ((r² - d²) / (r² - d² + |m|²))² · m        d = |x - c|
```

That ratio is flat in the middle and **steep at the rim**: it climbs from 0 to
nearly 1 over a band only about `|m|²/2r` wide. Sampling the axial backward map
numerically, it is non-monotonic — folded — for every `|m|` below about
`0.55 r`, and the fold *peaks at small displacements*:

```
|m|/r    0.10   0.20   0.30   0.45   0.50   0.55
fold      .044   .052   .041   .013   .005   0      (in units of r)
```

So the intuitive rule "keep the displacement well under the radius" is backwards
for this falloff. Replacing it with a falloff that is flat at both ends,
`1 - t²(3 - 2t)` with `t = d/r`, folds nowhere below `|m| = 2r/3`, and its
handle has an exact fixed point instead of an approximate one.

## Why it matters

The fold is a thin ring inside each handle where a few percent of `r` worth of
source content is sampled twice. It renders as a faint crease or a ripple, and
because every handle is individually correct and the image looks fine at high
strength, it reads as a bad mask, a bad mesh, or camera noise. Turning the
effect *down* to investigate makes it worse.

## How to apply

- Use a falloff with zero slope at the rim — `1 - t²(3 - 2t)`, a raised cosine,
  anything C¹ — for both translation and radial-scale handles. The same
  property is what lets primitives sum into a field with no creases
  ([[raised-cosine-contours-compose-without-seams]]).
- Derive the safe cap from the falloff's own steepest slope: injective while
  `|m| · max|S'| < r`. For `1 - t²(3 - 2t)` that maximum is `1.5`, hence `2r/3`.
- Centre a translation handle on the *destination*; then `u(c) = c - m` exactly,
  which is also a one-line assertion in a test.
- Assert the fold threshold in a test rather than trusting the cap: walk the
  axial backward map and require a strictly positive slope.
