---
title: A score curve evaluated at the mean error misstates the mean score
tags: [game-design, balance, statistics]
added: 2026-10-03
sources:
  - https://en.wikipedia.org/wiki/Jensen%27s_inequality
---

## Fact

For a nonlinear scoring function `f(error)`, the score at the average error is
not the average score: `f(E[error]) ≠ E[f(error)]`. With a decaying curve such
as `1000 · exp(−d² / 2σ²)`, the near misses in the error distribution dominate
the mean. Scoring uniformly random answers in RGB space at their mean distance
(≈169) gives ≈20 points, but random answers actually average ≈110 — over five
times more.

The degenerate strategy does even better: always answering the midpoint
minimises expected distance and averages ≈180 under the same curve.

## Why it matters

Balance claims written from the mean error ("guessing earns almost nothing")
end up in rules text, tutorials and test comments, and are wrong by a large
factor. The floor that a lazy or random player gets is set by the whole
distribution, not by its centre, so a curve tuned this way leaks more points
to non-skill play than intended.

## How to apply

- Calibrate by Monte Carlo over the real error distribution: sample answers,
  score each, average the scores. A few hundred thousand samples take
  milliseconds.
- Always measure the baselines, not just random: a constant answer (midpoint,
  most common value) is often the strongest no-skill strategy.
- When documenting a curve, quote scores at named errors ("off by 20 on every
  channel ≈ 850") and measured averages for strategies — never a score at the
  mean error presented as a typical result.
