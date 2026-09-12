---
title: A continuous payout rounded at every tick pays out nothing
tags: [game-design, numerics, simulation]
added: 2026-09-12
---

## Fact

Crediting a rate into an integer total once per frame silently floors to zero
whenever a single frame's share is below one unit:

```js
score += Math.round(elapsed * pointsPerSecond * multiplier);  // 0.41 -> 0
```

At 60 Hz, a payout of 25 points per beat is about 0.4 points a frame, so holding
a note for two full seconds is worth exactly nothing. Raising the frame rate
makes it worse rather than better, because every increment gets smaller.

## Why it matters

The failure scales with the *quality* of the implementation. A coarse four-times-
a-second update would have paid out; a smooth per-frame one does not. So it
arrives during a refactor toward smoothness, which is the last place anyone looks
for a scoring bug.

It also reads as a design complaint rather than an arithmetic one — "holding a
note isn't worth anything" sounds like balance, and the balance numbers are all
correct.

## How to apply

- Keep the running total in floating point and round only where it is displayed.
- Or carry the remainder explicitly, which keeps the total both exact and
  integral:

  ```js
  fraction += elapsed * pointsPerSecond * multiplier;
  const whole = Math.floor(fraction);
  total += whole;
  fraction -= whole;
  ```

- Assert the payout over a realistic *duration* against a competing case — a
  full hold must beat an early release. Asserting that one tick credited
  something tests the tick size, not the mechanism, and passes on the broken
  version whenever the rate happens to clear one unit per tick.
