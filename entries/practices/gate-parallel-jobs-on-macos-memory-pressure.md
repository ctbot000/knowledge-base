---
title: On macOS, hold back parallel jobs on the kernel's memory pressure level, not on free memory
tags: [testing, macos, memory, parallelism]
added: 2026-10-25
sources:
  - https://developer.apple.com/documentation/dispatch/dispatchsource/memorypressureevent
  - https://ss64.com/mac/memory_pressure.html
---

## Fact

A job runner that starts as many jobs as there are cores ignores memory, and on
macOS free memory cannot tell it when to stop: it sits at a few hundred MB on a
healthy machine, because the rest is cached or compressed.
`sysctl -n kern.memorystatus_vm_pressure_level` can: 1 is normal, 2 is warning,
4 is critical. It turns to warning as the kernel starts compressing and
swapping hard. The pressure level is what Activity Monitor's graph and
`DispatchSource.makeMemoryPressureSource` report.

## Why it matters

Browser test shards take 1 to 1.5 GB each. On a machine already low on memory,
a suite that finishes in under three minutes ran for over twenty, with load
average near 300 while CPU sat a third idle: threads waiting on page-ins count
towards the load.

## How to apply

- Before starting another job while some are already running, read the level.
  At 2 or above, wait (poll every couple of seconds or when a job ends). Never
  hold the first job, so the run cannot stall.
- Expect it to oscillate: the runner drains a few jobs, then refills. That
  costs a little time on a busy machine and nothing on a quiet one.
- On Linux, `os.freemem()` (MemAvailable) is a usable signal instead.
- Load average alone misleads here: check `vm.swapusage`, the compressor size
  in `top -l 1`, and CPU idle before concluding something is CPU-bound.
