---
title: A fluctuating value every client must agree on can be a pure function of the clock
tags: [simulation, game-design, randomness, multiplayer]
added: 2026-11-05
---

## Fact

Prices, weather or anything else that wanders can be computed from the time alone:
smooth noise layers keyed by `floor(t / period)` plus events hashed from time buckets.
Every client then shows the same value at the same moment with no server, no sync and
no stored history.

## Why it matters

The usual model, a random walk stepped from the last value, needs one authority to hold
the state and has no way to answer "what was it last Tuesday" without replaying from the
start. A pure function runs on static hosting and offline, draws any chart by just asking
for each point, and makes every test deterministic. It also keeps the value in bounds for
ever, which a random walk does not.

## How to apply

- Quantize first (`at = floor(t / TICK) * TICK`), so the value is steady within a tick
  and clients with slightly different clocks rarely disagree.
- Layer value noise: for each `[period, size]`, hash `floor(at / period)` and the next
  index, smoothstep between them, and sum. Add shared layers for what moves together.
- Events: hash each time bucket for "did one happen", when and how big, and add
  `size * min(1, since / rise) * exp(-since / fade)` over the buckets still in reach. The
  same hash yields the headline, and "not after t" keeps the future out of the news.
- Bound it softly: `base * exp(limit * tanh(x / limit))`.
- It mean-reverts by construction, so a cheap moment comes back and chart-reading pays;
  check the payoff with a simulated player before tuning. The trust boundary is the
  device clock, so this suits play money, not anything that must resist cheating.
