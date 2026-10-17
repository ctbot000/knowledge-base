---
title: Alpha-tested foliage thins out and vanishes with distance unless its texture covers more than the cutoff
tags: [graphics, webgl, textures, foliage]
added: 2026-10-17
sources:
  - https://bgolus.medium.com/anti-aliased-alpha-test-the-esoteric-alpha-to-coverage-8b177335ae4f
---

## Fact

Mipmapping averages alpha, and an alpha test compares that average against its
cutoff. A leaf card whose texture is under half opaque (with a 0.5 cutoff)
drops below it in the smaller mip levels, so far away the whole card is
discarded: crowns of trees and tufts of grass thin out with distance, then
disappear.

## Why it matters

Up close everything looks right, so the bug shows only on a distant view and
reads as a culling or level-of-detail problem. Sparse, delicate leaf
pictures, the ones that look best up close, fail first.

## How to apply

- Paint each card so that more of it is opaque than the cutoff (about 55-70%
  for a 0.5 cutoff): bigger, overlapping leaves rather than a few small ones.
- Or keep coverage per mip level: rescale each mip's alpha so the share of
  texels past the cutoff matches the base level, or use alpha-to-coverage
  with MSAA.
- Check foliage from far away, not only up close.
