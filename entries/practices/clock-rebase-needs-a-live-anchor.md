---
title: A clock that switches sources must rebase from a live reading, not from the value it last returned
tags: [clocks, web-audio, frontend]
added: 2026-09-12
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/currentTime
---

## Fact

A clock stitched from two sources — an audio context while it runs and a wall
clock while it is suspended, a server time while connected and a local one
offline — must stay continuous across the handover. The tempting anchor is the
value it last handed out:

```js
if (leavingA) { anchor = last; anchorWall = wall(); }   // wrong
```

`last` is only as fresh as its last *caller*. A clock read every frame during
play and not at all on a menu screen is stale by however long the app sat idle,
and the handover then rewinds it by exactly that gap. Anchor on a reading taken
at the transition instead:

```js
if (leavingA) { anchor = readA(); anchorWall = wall(); }
```

The source being left is usually still readable: a suspended `AudioContext`
keeps reporting `currentTime`, frozen at the instant it stopped.

## Why it matters

The jump needs an idle period before the transition, so it never reproduces
while you are actively driving the app — which is exactly how a clock gets
tested. And the clock is correct on both sides of the seam, so every downstream
symptom points somewhere else.

## How to apply

- Make the clock a pure function of its live source: `t = source() + offset`,
  with `offset` recomputed at transitions from live readings of both sides.
  Then no memoised output exists to anchor on by mistake.
- Keep the two timelines explicit. If the app clock is `source + offset`,
  anything scheduled on the *source's* own timeline has to subtract the offset
  back out.
- Exercise the transition after an idle gap, not right after driving the clock.

Related: [[suspended-audiocontext-freezes-currenttime]],
[[absolute-timeline-absorbs-a-jump-by-moving-its-epoch]].
