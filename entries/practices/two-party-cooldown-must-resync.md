---
title: A cooldown shared by two parties drifts out of phase unless a failed attempt resets both clocks
tags: [simulation, game-design, timers]
added: 2026-09-19
---

## Fact

When an action needs two participants that each hold their own cooldown, the
natural retry — push *my* deadline out and try again later — puts the pair into
a permanent leapfrog:

```js
if (now >= a.nextTry) {
  const mate = partners.find((o) => now >= o.nextTry);   // b is still cooling
  if (mate) doTheThing(a, mate);
  else a.nextTry = now + INTERVAL;                       // only a moves
}
```

`a` wakes while `b` is cooling, so `a` jumps ahead; `b` then wakes while `a` is
cooling and jumps further ahead. Neither is ever ready at the same moment as the
other, and a pair that satisfies every precondition never acts at all.

It is stable only while the deadlines happen to coincide, which is why it works
at first — both clocks are armed together at creation — and breaks the moment
anything moves one of them alone.

## Why it matters

Nothing is out of range and nothing throws. Every participant is healthy, every
threshold is met, and the arithmetic on each timer is correct in isolation, so
the search goes to the preconditions — and they are all innocent.

It also survives a single-seed test. Some starting offsets do line up, so the
behaviour appears in a fraction of runs, which reads as rarity rather than as a
deadlock.

## How to apply

- On failure, write the deadline of **every** party the attempt considered, not
  only the one whose timer fired.
- When no partner is ready, align to the earliest partner deadline rather than
  adding a fresh interval: `a.next = Math.max(now + INTERVAL, minPartnerNext)`.
- Sweep seeds, not one. "Did the pair ever act?" across a dozen runs catches
  this; a single run reports a plausible no.

Related: [[cooldown-fires-on-precondition]], [[sim-deadlines-in-sim-time]].
