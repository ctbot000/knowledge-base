---
title: Base-ten tick steps put a duration axis in seconds at 200 s, labelled 3 min 20 s
tags: [charts, chartjs, d3, dataviz]
added: 2026-11-09
sources:
  - https://github.com/chartjs/Chart.js/blob/master/src/helpers/helpers.math.ts
  - https://d3js.org/d3-array/ticks
---

## Fact

Chart.js's linear scale (`niceNum`) and d3's `ticks()` space ticks by 1, 2 or
5 times a power of ten, in the data's own unit. Durations plotted in seconds
therefore tick at 200 s or 500 s, and a formatter that prints minutes labels
the axis 3 min 20 s, 6 min 40 s, 10 min.

## Why it matters

Nothing errors and the bars are right, but the axis reads as arbitrary: nobody
estimates a value against "3 min 20 s". Changing the number of ticks only picks
another base-ten step, and none of those is a whole number of minutes (60 has a
factor of 3; 1, 2 and 5 × 10ⁿ never do).

## How to apply

- Plot in the unit whose round numbers you want: minutes for runs that take
  minutes (`ms / 60000`), hours for ones that take hours, and format the tick
  (`v => duration(v * 60000)`); fractions come out as 0.5, 1, 1.5, which read
  as 30 s, 1 min, 1 min 30 s.
- Or keep seconds and set the step yourself: Chart.js `ticks.stepSize: 60`
  (pick a multiple from the range), or your own tick values in d3.
- Clock times are a different case: a time scale (`type: 'time'`,
  `d3.scaleTime`) already steps in calendar units.
