---
title: A level terrace cut into a slope always has a steep uphill bank, and no blend shape avoids it
tags: [terrain, level-design, graphics, game-design]
added: 2026-09-12
---

## Fact

Flatten a strip of a slope `g` by blending the height field toward a constant
over a half-width `W`. The terrace holds height while the ground keeps rising,
so the `g·W` it cut away has to be given back within the blend. The *average*
slope across the give-back is therefore `g` no matter what, and because the
blend is flat in the middle the *peak* is worse than the average.

Measured across cut depths from 60% to 95% and window shapes from a bare cosine
to a wide flat-topped one, the peak bank never came out below about **1.3x the
slope of the face it is cut into**, and a cosine window put it near 1.6x. A
comfortable trail on a 40 degree face has a 55-60 degree bank above it.

Widening the blend does not help: the cut depth `g·W` grows with `W` at the same
rate the distance to recover it does.

## Why it matters

It is normally discovered as a bug — an invisible wall along a path, an agent
that cannot leave a road, a character stuck in a trench — and then chased
through the blend function, where there is nothing to find. Knowing the bound
turns it into a design decision instead: a terrace is a corridor you leave
downhill, and leaving it uphill costs something.

The only real lever is how much you flatten. Keeping 30% of the cross slope
makes the path a graded traverse rather than a bench and takes roughly 30% off
the bank, at the cost of a path that is no longer level.

## How to apply

- Budget the bank before building the path: `bank ≈ 1.4 · g`. If that exceeds
  what the character can climb, the terrace will wall them in.
- Decide deliberately whether crossing the bank should be possible, and check it
  against the movement limits rather than assuming.
- Where the corridor must be enterable from above, do not flatten — mark a line
  that is already walkable and leave the surface alone.
