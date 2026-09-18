---
title: A log fed by change detection silently drops every repeated value
tags: [observability, debugging, ui]
added: 2026-09-18
---

## Fact

`if (value !== previous) record(value)` is not a record of writes. It records
*distinct consecutive* writes, so a write that stores the value already sitting
there leaves no trace. The same blind spot swallows the first write whenever it
happens to match the field's initial value.

It stays quiet because the output still looks like output. A program emitting
1, 1, 2, 3, 5, 8 through such a filter logs 1, 2, 3, 5, 8 — one element short,
in a sequence that still reads as a sequence.

## Why it matters

Every symptom points at the thing being observed rather than at the observer:
a loop that seems to skip an iteration, a counter that seems off by one, a
duplicate that seems to have been de-duplicated on purpose. The producer is
correct and gets debugged anyway, sometimes for a long time, because the
recording code is not where anyone looks for a missing record.

## How to apply

Record on the event, not on the delta — the write call, the setter, the control
signal that commanded the store. Where only polling is available, compare a
monotonically increasing write counter or sequence number rather than the value,
and log when *that* moves.
