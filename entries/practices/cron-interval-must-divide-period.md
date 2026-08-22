---
title: Cron cannot express an every-N-hours interval unless N divides 24
tags: [cron, scheduling, automation]
added: 2026-08-22
---

## Fact

A cron step value is a filter over a fixed calendar field, not an interval timer.
`0 */5 * * *` does not mean "every 5 hours" — it selects the hours matching
`h % 5 == 0`, i.e. 00, 05, 10, 15, 20, and then wraps to 00 the next day. Four
gaps of 5 hours, then one of 4.

The same holds for every field whose range is not a multiple of the step:
`*/7 * * * *` gives 7-minute gaps until :56, then a 4-minute one. Only steps that
divide the field's period evenly (2, 3, 4, 6, 8, 12 for hours; 2, 3, 4, 5, 6, 10,
12, 15, 20, 30 for minutes) produce a uniform interval.

## Why it matters

The short interval at the wrap point is silent — the job fires, nothing errors,
and the schedule looks correct in every listing. It surfaces only as a job that
occasionally runs too soon: a duplicate notification, a polling window that
overlaps the previous one, a token refreshed before the old one expired, or a
rate-limit window opened early and wasted.

It is also invisible in testing, because the anomaly happens once per day at a
specific wall-clock boundary rather than on every run.

## How to apply

- Check that the step divides the field's period. If it does not, cron is the
  wrong tool for that interval — do not try to patch it with a longer expression.
- Enumerate the fire times explicitly when the drift is tolerable and you want a
  fixed daily rhythm: `0 1,6,11,16,21 * * *` is honest about where the short gap
  falls, unlike `*/5`.
- For a true interval, use a **self-rescheduling one-shot**: the job runs, then
  computes `now + N` and re-arms itself for that single time. Each run re-anchors
  from when it actually fired, so the interval stays exact and the schedule
  self-corrects after a missed or delayed run. This is the only form that
  survives the scheduler being offline at a due time.
- Prefer a scheduler with native interval support when one is available; the
  constraint is cron's calendar-filter model, not scheduling in general. On Linux
  that is systemd's `OnUnitActiveSec`; on macOS it is a launchd agent's
  `StartInterval` (seconds between runs, re-anchored from the last fire); most job
  queues expose an `every`. All three express the interval cron cannot.
