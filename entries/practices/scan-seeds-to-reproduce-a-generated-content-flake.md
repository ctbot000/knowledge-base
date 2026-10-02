---
title: A rare failure on generated content reproduces every time once you scan seeds offline for the coordinates it reported
tags: [testing, flaky-tests, debugging, procedural-generation]
added: 2026-10-02
---

## Fact

When a test fails now and then on randomly generated content (a world, a level,
seeded data) and its message names a concrete value, such as a cell, a position
or an id, that value fingerprints the layout. Running the generator on its own
over thousands of seeds, with the test's own placement logic on top, and keeping
the seeds that put the suspected condition at that value finds one that fails
every time, typically in seconds and without the app or a browser.

## Why it matters

Reruns pass, so the failure gets filed as timing flakiness, and a fix can only
be judged by looping the test hundreds of times for a 1% event. With a pinned
seed it is an ordinary failing test: the cause can be read off directly (for
example, a target chosen as a column's highest solid block lying under water,
or being a treetop), and the old code failing on that seed while the fix passes
is the proof.

## How to apply

- Import the generator outside the app (seed in, content out) and replay what
  the test does on top of it: the spawn, the offsets, a walk modelled as a
  straight line. A crude model is fine for finding candidates.
- Filter for the exact reported value plus the condition you suspect, then
  print the matching seeds.
- Pin a match in the real run, through a seed option or by stubbing the random
  source only around the call that draws the seed, and confirm the old code
  fails there before trusting the fix.
- Put the seed in the failure message, so the next one needs no search.
