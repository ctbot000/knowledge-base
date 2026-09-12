---
title: A difficulty curve is not monotonic in any single resource, so a test must assert the trend
tags: [game-design, testing, level-design]
added: 2026-09-12
---

## Fact

Authored difficulty is tempting to guard with a one-line invariant: total
enemy health, or total obstacle count, must rise with every level. It fails
immediately on good design, because a well-built curve periodically **trades
one resource for a different threat** — the first level that introduces a new
mechanic usually costs less of the old resource, and reads as a dip.

A finale that spikes creates the mirror problem: whatever follows it, including
the first level of an endless or new-game-plus mode, is lower than its
predecessor by design.

## Why it matters

The assertion fails on exactly the content it was written to protect: the
interesting levels. The natural response is to inflate the dipping level back
over its neighbour, which flattens the variety the dip existed to create.

## How to apply

- Assert the trend over a window, not wave on wave:
  `resource(n) > resource(n - k)`, with `k` at least as long as the design's
  own repeating cycle. If bosses land every fifth level, compare across five,
  so each level is compared with the same phase of the cycle.
- Assert separately that nothing *collapses* —
  `resource(n) > resource(n - 1) * 0.5` — which is the real failure that the
  monotonic rule was reaching for.
- Assert the shape you actually intend: that the last authored level is the
  peak, and that a procedural tail eventually surpasses it.
- If a dip is deliberate, the invariant should say which resource is being
  traded for what, rather than being loosened until it passes.
