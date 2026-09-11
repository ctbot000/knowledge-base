---
title: An obstacle that forces one input must fit inside the band where only that input works
tags: [game-design, collision, level-design]
added: 2026-09-06
updated: 2026-09-11
---

## Fact

When a defensive action changes the player's hitbox — ducking, sliding,
crouching — the obstacles that are supposed to require it are constrained to a
narrow band, and the band is arithmetic rather than taste.

With a standing box 50 tall, a ducking box 28 tall and a 4px collision inset,
the only heights that force a duck are those whose lower edge sits below the
standing head and above the ducking one: a 22px window. An obstacle placed
outside it is either free to run under or impossible to avoid, and one that
straddles an edge changes category depending on where it happens to be.

Vertical animation is what usually breaks it. A bob of ±9px on a 22px window
swings the obstacle across both boundaries, so the same obstacle is sometimes
duckable and sometimes not, with nothing on screen to say which.

The band has a ceiling as well as a floor, and the ceiling is set by every
*combination* of movement verbs, not by the obvious one. A barrier placed above
a single jump's apex is still answered by a double jump, which reaches roughly
1.8x as high when the second jump is timed near the first's apex — so a wall
meant to force a sidestep quietly becomes jumpable, and the movement axis it
existed to justify becomes decoration.

## Why it matters

The failure does not look like a geometry error. It looks like inconsistent
collision or bad luck: the player does the correct thing, dies anyway, and
cannot tell why. That is the most expensive kind of unfairness, because it
teaches the player that the rule they just learned is unreliable.

It also hides from playtesting, since most placements land safely inside the
band and only the extremes of the animation fail.

## How to apply

- Compute the band from the two hitboxes and the insets before placing
  anything, and place the obstacle at its centre rather than by eye.
- Measure the ceiling rather than deriving it: sweep the timing of the second
  jump (or dash, or wall-kick) across its whole range in the simulation and
  take the maximum reached. Chained verbs interact through the state they leave
  each other, so the closed form for one of them is not the answer.
- Keep any animation amplitude well inside the band — a couple of pixels for
  life, not a swing that reaches an edge. Move the wings, not the body.
- Give the "must jump" variant the opposite test: it has to overlap the
  standing *and* the ducking box, or ducking silently becomes a second answer.
- Where two answers are intended, make both clear the obstacle at every point
  of its animation, and verify by simulation rather than by playing it once.
- Assert the negative directly: for an obstacle meant to have exactly one
  answer, sweep every other verb at every timing and require all of them to
  fail. It is a short test and it is the only thing that keeps a new movement
  mechanic load-bearing.
