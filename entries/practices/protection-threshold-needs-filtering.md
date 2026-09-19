---
title: A protection threshold read from an instantaneous measurement fires on the transient the system exists to produce
tags: [control, simulation, monitoring, reliability]
added: 2026-09-20
---

## Fact

Protections are written against a slow condition — the resource is running out,
the component is overheating, the queue is falling behind — but they are
usually wired to the live reading of a signal that also moves *fast* under
load. The two are not separable by threshold alone, because the deepest
excursion coincides with peak demand.

A battery is the clearest case. Pack voltage falls with charge over minutes,
and also falls with current within milliseconds: a full pack pulling its peak
current sags as far as a nearly empty one at rest. A cutoff reading live
voltage therefore triggers during hard acceleration, on a pack that is
four-fifths full, which is the one moment the protection must not act.

## Why it matters

The protection fires precisely during the activity it was meant to safeguard,
so the system looks unusable at exactly its intended operating point, and the
symptom is attributed to whatever the operator was doing at the time.

Raising the threshold does not fix it and makes the real condition undetectable;
the two failure modes bracket a window that may not exist at all. The signal
needs separating in the *frequency* domain, not in the value domain.

## How to apply

- Low-pass the signal the protection reads, with a corner well below the
  transient it must ignore, and keep the unfiltered value for display. Fast
  reading for the operator, slow reading for the latch.
- Require the condition to persist before acting. A dwell of a second or two
  costs nothing against a condition that takes minutes to develop.
- Add a second, independent measure of the slow quantity — charge consumed,
  energy integrated, time in service — and require both. A transient can move
  one of them, not both.
- Test it with the worst legitimate transient, not with the fault. If full
  demand on a healthy system trips the protection, the threshold is measuring
  the wrong thing.
