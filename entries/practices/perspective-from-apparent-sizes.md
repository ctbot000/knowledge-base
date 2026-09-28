---
title: Three points and their apparent sizes predict a fourth point of a tilted plane far better than a parallelogram
tags: [geometry, computer-vision, image-processing]
added: 2026-09-28
sources:
  - https://en.wikipedia.org/wiki/Homography_(computer_vision)
---

## Fact

A plane seen through a camera maps to the image as `p = N(u, v) / w(u, v)`,
with `N` and `w` both affine in plane coordinates. `w` is proportional to depth,
and a feature's apparent size is roughly proportional to `1/w`. So three
reference points with known plane coordinates and measured sizes `s_i` fix
the perspective. Weight each point's image position by `1/s_i`, take the affine
combination the target has in plane coordinates, do the same with the weights,
and divide. The parallelogram rule is the special case of equal sizes.

## Why it matters

With only three fiducials (a QR code's finder patterns, three marker corners)
the usual guess for the fourth corner, `B + C - A`, ignores foreshortening.
Under a modest tilt it misses by several module widths. That is enough to
put the search for the real feature in the wrong place, or to sample a grid that
cannot be decoded.

## How to apply

```js
// Target at A + alpha (B - A) + beta (C - A) in plane coordinates, where
// A, B, C are image points with apparent sizes sA, sB, sC. y likewise.
const [wA, wB, wC] = [1 / sA, 1 / sB, 1 / sC];
const d = wA + alpha * (wB - wA) + beta * (wC - wA);
const x = (A.x * wA + alpha * (B.x * wB - A.x * wA) + beta * (C.x * wC - A.x * wA)) / d;
```

- Measure sizes along the plane's own axes. A size taken along image rows is
  inflated by rotation.
- Use it to aim a search, then refine with a real correspondence. The
  size-to-depth link is only approximate.
