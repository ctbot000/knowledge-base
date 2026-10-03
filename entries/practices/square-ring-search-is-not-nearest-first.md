---
title: A search outward in growing square rings is not nearest-first
tags: [algorithms, grids, game-design]
added: 2026-10-03
---

## Fact

Searching a grid outward in square rings (every cell at Chebyshev distance
`r`, then `r + 1`) is the usual way to find the nearest cell that qualifies.
Returning the first match is not nearest-first, in two ways:

- Within a ring, the loop order decides. A corner of ring `r` is `r√2` away
  and its edge midpoints only `r`, and a loop that starts at `(-r, -r)` meets
  the corner first.
- Across rings, ring `r + 1` holds cells `r + 1` away, which is nearer than
  ring `r`'s corners once `r ≥ 3`, since `r√2 > r + 1`.

## Why it matters

The answer is always close and always valid, so it looks right. It shows up as
something placed a little to one side, such as a creature appearing at the far
corner of a pool instead of at the edge that was tapped. That reads as a
placement quirk, not as a search bug.

## How to apply

- Keep the best match by true (Euclidean) distance, skip cells that cannot
  beat it, and stop only once the ring index is past the best distance found.
- Test with a target whose nearest qualifying cell is straight ahead on a
  ring's edge while the same ring also has qualifying corners.
