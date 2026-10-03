---
title: A record a new device creates by default must carry the oldest timestamp, or last-writer-wins sync spreads it over the real one
tags: [sync, data-loss, distributed-systems]
added: 2026-10-03
sources:
  - https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set_(Last-Write-Wins-Element-Set)
---

## Fact

In last-writer-wins (LWW) sync, the copy with the newer change timestamp
wins. A device that starts without the user's data usually creates a
placeholder (a random name, default settings) and stamps it `now()`, which
is newer than every real edit, so the first sync replaces the user's real
record with the placeholder, on every device.

## Why it matters

Signing in on a second device, reinstalling, or clearing storage silently
resets the user's profile everywhere. Nothing fails: the placeholder simply
looks like the latest edit.

## How to apply

- Stamp generated defaults with 0 ("never edited") and set the timestamp
  only when the user edits the record.
- Bump it only for fields the user edits (a name, an avatar), not for
  counters or flags the app updates by itself, or every device always looks
  newest.
- Merge accumulating fields monotonically instead of by LWW (a union of
  earned items keeping the earliest date, the maximum of each counter), so
  no device loses progress whichever side wins.
- When a device signs in to an existing account, seed its local record from
  the server's copy before the first sync, not from local defaults.
- Test that merging a fresh default with an older real record yields the
  real record, in both argument orders.
