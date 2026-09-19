---
title: A feedback flash retriggered faster than it decays is a constant state, not a flash
tags: [game-design, ui, animation]
added: 2026-09-19
---

## Fact

Visual acknowledgement is usually written as a value set to 1 on each event and
decayed per second, with the drawing code branching on it:

```js
onHit(e) { e.flash = 1; }
draw(e)  { ctx.fillStyle = e.flash > 0.1 ? '#fff' : e.color; }
```

That is a flash only while events arrive more slowly than the decay. Once the
retrigger interval drops below the decay time the value never falls, and the
branch is permanently on: a boss under four-barrel fire is hit roughly thirty
times a second against a decay of five per second, so it is white for the whole
fight and its own colour never appears.

The same shape turns a "recently changed" row highlight into a permanently
highlighted table, and a toast into a banner.

## Why it matters

It is invisible at the rate the feature was built against — one hit, one flash,
looks perfect — and appears only at the rate the finished product actually
runs at. The artwork underneath is never seen, so it reads as a palette or
asset problem rather than a timing one.

Because the effect is *always* on, it also stops carrying information: the
player can no longer tell a hit from a miss, which is the entire point.

## How to apply

- Interpolate instead of branching: mix towards the highlight colour by the
  flash value, so a saturated flash still shows the object's identity.
- Cap the mix well below 1 (40–60% is plenty) for anything that can be
  retriggered rapidly.
- Compare the two numbers directly when tuning: decay rate must exceed the
  worst-case event rate, or the effect must be designed to look correct while
  held on.
- Where the flash must stay discrete, latch it for a fixed duration and ignore
  retriggers inside that window, rather than resetting the value.
