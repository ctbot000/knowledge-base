---
title: Playing a multi-scale process back in log time spends the run where the process is slowest
tags: [animation, visualisation, simulation]
added: 2026-09-19
---

## Fact

A process spanning many orders of magnitude gets animated at a constant rate in
log time, because that is the only way to show all of it. The pacing that
results is set by the underlying power law, not by where anything happens.

Cosmic history is the clean case. During radiation domination the scale factor
grows as the square root of time, so a fixed span in `log a` costs twice as
much in `log t`. The quark epoch spans about eighteen decades of `a` and
therefore about thirty-seven of the sixty-two decades of `t`: a constant-rate
playback spends **sixty percent of its run** on one unchanging image, then
crosses recombination — the visually decisive moment — in under a second.

## Why it matters

It reads as a content problem rather than a pacing one. The obvious responses
all make it worse: adding detail to the long stretch, or speeding the whole
thing up until the interesting part is gone entirely. Meanwhile the animation
is *correct*, so there is nothing to debug.

## How to apply

- Reparameterise on a position `u` in [0, 1] and map it piecewise-linearly onto
  the boundaries of the phases you want seen, so each phase gets an equal share
  of wall-clock time.
- Keep every readout in the true variable. The warp is presentational; a
  scrubber may be non-uniform, but the number beside it must be real.
- Build the knot list from the phase table already in the model, and clamp it to
  the range actually reachable for the current parameters, so configurations
  that skip a phase do not get a dead segment.
- The same fix applies to any log-scale scrubber: geological time, exponential
  decay, a zoom through length scales.
