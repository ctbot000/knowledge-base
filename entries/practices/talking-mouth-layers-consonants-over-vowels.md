---
title: A talking mouth closes fully only when consonants are laid over the vowel movement, not averaged with it
tags: [animation, speech, lip-sync, procedural]
added: 2026-11-26
sources:
  - https://doi.org/10.1121/1.1910340
---

## Fact

Speech is one continuous vowel-to-vowel movement with consonants superimposed
(Öhman 1967). Animate it that way: interpolate between held vowel poses across
everything in between, then for each consonant in turn mix its pose in with a
weight per articulator that ramps to exactly 1 and back. Where the weight is 1
the target is met exactly, and where it is 0 (the tongue during `p`) the vowel
movement shows through. Weighted averages of neighbouring poses never reach any
of them.

## Why it matters

A viewer forgives a vowel that is a little off, and not lips that fail to meet on
`m` or a tongue that stops short of the teeth. With averaged poses the closures
are the part that is always wrong, and raising their weight to fix it makes every
neighbouring vowel snap. Anticipation (lips already round in the `t` of "two")
also comes free from the vowel layer instead of from hand-written rules.

## How to apply

- Ramp with a minimum-jerk step. Start a stop's ramp before the sound and hold
  it at 1 from the closure to the release, not over the whole phoneme.
- Apply glides and liquids first and stops, fricatives and nasals after them, or
  an early `r` pulls the `k` before it open.
- Give velum and voicing tracks of their own, with their own timing.
- Test it on real timings: at the key moment of every `p b m` the lips' gap is
  below a millimetre, and no point moves faster than about 0.5 m/s.
