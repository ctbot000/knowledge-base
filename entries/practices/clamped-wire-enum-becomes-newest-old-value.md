---
title: A clamp on an enum sent over the wire turns every new value into the newest old one
tags: [networking, protocol, testing]
added: 2026-11-06
---

## Fact

A server or relay that bounds an enum field with `min(max, value)`, rather than
checking it against the list of values, passes a newly added value on as the
last value it knew. Nothing fails: the message is valid, the field is in range,
and the receiver does exactly what it was told, only the wrong thing.

## Why it matters

The sender never sees it. Its own copy of the state does not go through the
relay, so the feature looks right on the machine it was written on, and every
single-client test passes. Only a second client shows the fault, as something
plausible but unrelated: one player's new animation appears to their friends as
whichever animation was added before it.

The bound is also far from the enum, written as a bare number, so adding a value
gives no hint that it exists.

## How to apply

- Validate by membership, and send an unknown value to a neutral default rather
  than to the nearest valid one, so that a stale relay degrades visibly and
  harmlessly.
- If the bound stays, derive it from the enum's own definition where the code can
  share it.
- Either way, test the round trip: send every value of the enum through the relay
  and read it on the other side. That test fails the day a value is added, on the
  machine of whoever added it.
