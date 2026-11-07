---
title: A blink counted back from its end starts in whatever phase its length leaves it
tags: [game-design, animation, ui]
added: 2026-11-07
---

## Fact

`on = floor((until - now) / period) % 2 === 0` is the short way to write a blink,
and it is on or off at the start according to the length of the whole effect. With
a 75 ms period, 370 ms starts on; 420 ms starts off for 45 ms; 450 ms is on for a
single frame and then off for 75 ms.

## Why it matters

Feedback that must land on the first frame misses it, and only for some durations.
When the length is tuned per weapon or scaled up for bigger events, the heaviest
blows are the ones that can start with no flash at all. It never shows in a code
read and is too quick to catch by eye.

## How to apply

- Count from the start, or make the first stretch explicit: solid while the impact
  lasts, and blink only in a fixed tail counted back from the end.
- `on = left > TAIL || floor(left / (TAIL / 3)) === 1` is solid, then off, on, off,
  whatever the total length.
- Assert the first frame, for each duration in use.
