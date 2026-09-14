---
title: A solvability test cannot see a trivially solvable instance
tags: [procedural-generation, puzzles, testing]
added: 2026-09-14
---

## Fact

The usual guard on a puzzle generator is a solver that plays every seed through.
It answers one question — *can this be solved?* — and a degenerate instance
answers it just as cheerfully as a good one. A subset-sum whose rack happens to
contain a weight equal to the target is solvable, and solved in one click.

Degeneracy usually arrives from two places, both of which look harmless in the
generator:

```js
// 1. a fallback, taken on the seeds where the clever path failed
if (sum(chosen) !== target) chosen = [target];

// 2. distractors drawn without reference to the answer
const decoys = shuffle(all).filter((w) => !chosen.includes(w));  // one may BE the target
```

The first fires on a minority of seeds, which is exactly the minority nobody
plays while developing. The second fires whenever the distractor pool can
contain the answer.

## Why it matters

Nothing is broken, so nothing reports anything: the generator returns, the
solver solves, the suite is green, and a share of your players get a puzzle that
is not a puzzle. It is invisible to a seed-sweep test because *solvable* is the
only property being asserted, and the degenerate instances are the most solvable
of all.

It is also invisible at the desk. You test the seeds you happen to load, and
"that one was easy" is not a thought that survives to the bug tracker.

## How to apply

- **Build the answer first, then derive the distractors from it.** Enumerate the
  valid answers, pick one, and generate the rest of the instance to be
  consistent with — and constrained against — that choice. A generator that
  makes candidates and hopes an answer exists needs a fallback, and fallbacks
  are where degeneracy lives.
- **Assert the shape of the answer, not just its existence.** "At least two
  elements are needed", "no single element is the whole answer", "the scrambled
  grid is not already connected". These are one line each and they are what the
  solvability test cannot say.
- Sweep seeds for the *distribution*, not only for pass/fail: count how many
  ways each instance can be solved, and look at the histogram. A spike at one
  is the tell.
- See [[no-guess-puzzle-generation]] for the other half of the problem — whether
  the deductions exist at all — and [[puzzle-tests-must-parse-the-clue]] for
  whether the player is ever told them.
