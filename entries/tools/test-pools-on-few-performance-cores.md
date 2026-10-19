---
title: On a Mac with few performance cores, a test run that starts a process per core makes each test many times slower
tags: [testing, macos, performance, node, browser]
added: 2026-10-19
---

## Fact

Apple Silicon Macs have a handful of performance cores and more efficiency
cores. Run as many CPU-bound test files as there are cores (node --test does,
by default) next to browser tests, and most of them land on efficiency cores
while the browsers' GPU and renderer processes take the rest: files that take
1–3 s alone took 15–50 s, and a 16 s test 175 s.

## Why it matters

The whole run gets slower than it needs to be, and wall-clock waits that are
generous alone (a 3 s reply timeout, a 30 s page wait) run out, so the
contention reads as flaky tests. Timing a test inside such a run says nothing
about the test.

## How to apply

- Measure each file alone before optimizing it; contended numbers mislead.
- Run browser test shards few at a time (here 3 on 4+6 cores beat 2, 4 and 5)
  and start the longest jobs first, by the durations of the last run.
- Make waits that only bound a failure generous, so load cannot trip them.
