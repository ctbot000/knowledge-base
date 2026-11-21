---
title: A catch test that counts the target's recent positions cancels its dodges unless a dodge clears them
tags: [game-design, networking, ai, balance]
added: 2026-11-21
---

## Fact

To be fair to players who see a fleeing target drawn late (snapshot
interpolation puts it a few hundred milliseconds in the past), the authority
often counts a touch on any of the target's positions from that window — a
short trail behind it. That trail also follows the target through a sidestep:
for the whole window after a jink, the spot it jinked away from still counts
as the target. A pursuer who keeps running straight touches the old spot and
catches it, so the evasive move does nothing, and the extra reach (speed ×
window, ~1.5–2 m at running speeds) catches it from further off than it looks.

## Why it matters

The chase reads as trivially easy, and the obvious knobs — more dodges, faster
dodges, a smarter flee direction — barely move the time-to-catch, because the
catch was never decided by where the target is. It looks like an AI or tuning
problem; it is the hit test.

## How to apply

- When the target makes a deliberate discontinuous move (a jink, a blink, a
  leap), clear its trail at that moment. Players see the move a window late,
  so they also see the target "still there" briefly; that is the dodge
  landing, and it reads as one.
- Keep the window no longer than the drawing delay plus one snapshot; anything
  more is pure extra reach.
- Measure with a simulated pursuer that aims at where the target is *drawn*
  (delayed by the interpolation window) with per-decision aim error, and
  compare time-to-catch with the trail on and off: if a dodge changes nothing,
  this is why.
