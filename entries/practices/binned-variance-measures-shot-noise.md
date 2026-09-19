---
title: A density contrast measured by binning reports Poisson shot noise until you subtract it
tags: [statistics, simulation, instrumentation]
added: 2026-09-19
---

## Fact

Bin `N` points into `C` cells and the variance of the counts is not a property
of the points' arrangement alone. Even for a perfectly uniform random field,
each cell holds a Poisson count, so

```
sigma^2_measured  =  sigma^2_structure  +  1/mean       where mean = N / C
```

With 4096 particles in a 12x12x12 grid the mean is 2.4 and the noise floor is
`1/sqrt(2.4)` = 0.65. A freshly initialised simulation with no structure at all
reports a density contrast of 0.65, which looks like a plausible measurement
rather than a bug.

## Why it matters

The number is usually shown as "how clumpy is this" and read as physics. It
starts at the wrong value, and worse, it *moves the right way* as the
simulation runs, so nothing prompts a second look. Changing the particle count
to investigate makes it worse: more particles lower the floor, so the metric
appears to depend on resolution, which sends the search into the solver.

The same term contaminates any binned count statistic: histogram variance,
per-tile occupancy, request-rate jitter, heatmap contrast.

## How to apply

- Subtract the floor rather than choosing a grid that hides it:

  ```js
  const corrected = measured - 1 / mean;
  return corrected > 0 ? Math.sqrt(corrected) : 0;
  ```

- Size the grid from the sample, not from a constant, so the correction stays
  small: aim for roughly twenty per cell, `cells = cbrt(n / 20)`.
- Sanity-check by shuffling the points uniformly and re-measuring. A correct
  metric reads zero on the shuffle; an uncorrected one reads the floor.
- Clamp at zero. The corrected variance goes slightly negative on a
  sub-Poisson arrangement such as a lattice, and `sqrt` of that is NaN.
