---
title: In a board of bouncing obstacles the random walk's step size is set by the fall between rows, not by the obstacle spacing
tags: [simulation, physics, game-design]
added: 2026-09-22
---

## Fact

A Galton board, a pachinko field, a plinko wall: the intended behaviour is a
binomial walk, one column left or right per row. Built from ballistic bounces
it is not, because the lateral displacement after a deflection is

```
dx ~ v_x * t,   v_x ~ k * sqrt(2 g h),   t = sqrt(2 h / g)   =>   dx ~ 2 k h
```

— proportional to the **drop between rows**, and independent of the spacing the
columns were laid out with. A 45 px drop sends a deflected ball 40-60 px
sideways whatever the pegs are spaced at, so with a 50 px pitch every ball
crosses several columns per row.

Once outside the field of obstacles nothing brings it back, so the result is not
a wide bell curve: it is bimodal, everything piled against the two outer walls
with the middle empty.

## Why it matters

The shape is diagnostic and the instinct is wrong. Two piles at the edges looks
like a containment bug or a leak, so the walls, the bins and the collision code
get inspected first — and they are fine. Varying restitution, friction, obstacle
size and ball size all leave the distribution essentially unchanged, which is
the real clue: the term that dominates is not in any of them.

## How to apply

- Check `2 * h / spacing` before anything else. For a walk of one half-column
  per row it needs to be about 0.5, so the spacing wants to be roughly twice the
  drop. That is a wide, shallow-stepped board, which is what real ones are.
- Where the geometry cannot be that wide, add viscous drag so the balls reach a
  terminal velocity instead of free-falling. Damping of about `g / v_terminal`
  turns the same layout into a clean bell curve.
- Measure the standard deviation against the ideal `sqrt(rows) / 2 * spacing`
  rather than judging the pile by eye.
