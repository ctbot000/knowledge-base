---
title: A price rounded to whole units can be farmed across its rounding boundary
tags: [game-design, economy, numerics]
added: 2026-11-05
---

## Fact

With one rounded price for buying and selling, a real move of 0.1% across an `x.5`
boundary reads as a full unit, which is 5% on a 20-unit item. Round buy and sell
separately from a real spread, and force them apart, and no profit is possible without a
real move bigger than the spread.

## Why it matters

The exploit appears only on cheap items with a value sitting near a boundary, so a sweep
of average returns looks fine while a patient player or a bot prints money. A percentage
fee does not fix it on its own if the fee rounds to nothing at low prices.

## How to apply

```js
const sell = Math.max(1, Math.round(p * (1 - s)));
const buy = Math.max(sell + 1, Math.round(p * (1 + s)));
```

`sell(t2) > buy(t1)` then requires `p2 / p1 >= (1 + s) / (1 - s)`: rounding can shift each
side by at most half a unit, and the one-unit gap between integers absorbs both. Assert
exactly that over many moments in a test rather than the average return.

Count only the profit as "earned" for any lifetime total, or buying and selling in a
circle farms that instead.
