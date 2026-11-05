---
title: A stock split shows up as past closes restated, not as a jump in the price
tags: [market-data, finance, data-quality]
added: 2026-11-06
---

## Fact

Providers adjust daily history for splits, so after a ten-for-one split every earlier close
reads a tenth of what it did. Comparing a stored close for a finished day with the freshly
fetched one reveals the split and its ratio, even after days offline, with no corporate
actions feed.

## Why it matters

A holding kept as a share count loses 90% of its value overnight if the split is missed.
Looking for a big overnight fall in the series finds nothing, because the adjusted series
has no fall in it, and a real crash can look the same in unadjusted data.

## How to apply

- Compare only finished days: the newest day in a feed may still be trading.
- Treat a ratio as a split only when it lands near a tidy number (2, 3, 5, 10, or their
  inverses, within a few percent). Dividend adjustments are far smaller than the threshold.
- Apply it once per holding: keep when each holding last changed, and apply only splits
  after that, so shares bought at the new price stay as they are. Keep the cost basis
  unchanged and multiply the share count.
