---
title: A label keyed to a proxy variable contradicts the model as soon as the parameters leave the regime it was calibrated in
tags: [simulation, ui, modelling]
added: 2026-09-19
---

## Fact

Classifying state by a stand-in variable is cheap and usually right, because in
the default configuration the proxy tracks the thing. Change the parameters and
the two come apart, while the label keeps reporting with full confidence.

A cosmology view labelled its eras by scale factor alone. For the measured
universe that is correct: the present is the dark-energy era. Set the matter
density high enough to recollapse and the same code still displayed "Dark
energy era. Expansion is accelerating." beside its own readout of a positive
deceleration parameter and a fate of "Big Crunch".

## Why it matters

The contradiction is between two things on the same screen, both computed
correctly, so no test of either one catches it. It is also the output most
likely to be trusted: a label is prose, and prose reads as authored rather than
derived.

It only appears once someone moves a control away from the default, which is
exactly what an explorable model is for and exactly what is least exercised
during development.

## How to apply

- Separate the boundaries that are genuinely regime-independent from the ones
  that are not. Recombination happens at 3000 K whatever the expansion history;
  whether today accelerates is a fact about the parameters.
- Derive the parameter-dependent labels from the same quantity the readout
  shows, not from a correlate of it.
- Test the contradiction directly: assert that the narration for a recollapsing
  universe does not contain the word "accelerating".
- When a proxy really is the only thing available, say what it assumes in the
  label rather than asserting the conclusion.
