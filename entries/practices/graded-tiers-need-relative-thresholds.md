---
title: A difficulty tier defined by an absolute threshold is not a tier
tags: [game-design, procedural-generation, balance]
added: 2026-09-12
---

## Fact

Deriving graded variants of the same content by fixing a threshold per tier —
Easy keeps quarter notes, Medium keeps eighths, Expert keeps everything —
separates them only where the source is denser than the threshold. Where it is
not, the filter passes everything and two tiers become the same artefact.

Across three songs, tiers pinned to note grids produced Medium and Expert charts
within 1% of each other on every song already written in eighths. Each filter was
live and behaving exactly as specified.

Defining a tier as a *share of the full set* and solving for the threshold fixes
it:

```
target = round(fullCount * tierFraction)
choose the spacing from a ladder whose surviving count lands nearest target
```

which held the ratios at roughly 0.42 / 0.72 / 1.0 on every song.

## Why it matters

Absolute thresholds look right in review and test green, because each one does
precisely what it claims. The defect exists only *between* tiers and only for
some inputs, so a fixture that happens to be dense hides it completely, and the
setting reads as tuned while changing nothing.

It generalises well past difficulty, to anything offering graded variants over
author-supplied content: level-of-detail meshes, summary lengths, sampling rates,
preview qualities. Wherever the knob is absolute and the content is not, the
lower settings quietly stop being distinct.

## How to apply

- State each tier as a fraction of the full artefact, then solve for the
  parameter. Fractions are comparable across content; thresholds are not.
- Assert separation *between* adjacent tiers, not the properties of each one
  alone: every tier must be meaningfully denser than the one below it on every
  input, and the ordering must never invert.
- Pick which elements survive by a weight that means something in the domain
  (metrical strength, silhouette contribution, information gain). Otherwise a
  thinned tier is a random subset rather than a simpler rendition.

Related: [[min-gap-sets-density-not-bounds-it]], [[balance-knob-with-no-effect]].
