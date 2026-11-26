---
title: A server-decided random outcome shows the instant a client-predicted action lands if the server deals it one action ahead
tags: [networking, game-design, prediction, randomness]
added: 2026-11-27
---

## Fact

When a client plays an action's effects locally as it lands (hit-stop, sound,
damage word) but the server owns the dice (a critical hit, a lucky drop), a
roll made when the action reaches the server can only be shown a round trip
after the plain effect already played. Rolling one action ahead fixes that:
when action n arrives, the server rolls action n+1 and tells only that client,
which then knows the outcome before it acts, while the server still decides it.

## Why it matters

A special effect that arrives a beat late reads as lag or as a second hit, and
cannot lengthen a hit-stop that is already over. Letting the client roll hands
the outcome to anyone who edits the client. A seed shared with the client plus
two counters desyncs on one lost or rejected message, and lets a client skip
unlucky draws by spending them on actions that do nothing.

## How to apply

- Number actions on the client and send the number with the action and with
  everything it causes later (a projectile landing after the next action
  started); the server keeps the last few numbers' outcomes and looks them up.
- Tell the client only about the special outcome, naming its number; a notice
  that arrives after that action was sent names a used number and is ignored.
- Restart numbering on every (re)connect handshake. A client that sends no
  numbers never gets the outcome and a server that deals none never sends
  notices, so old and new versions agree on every action.
- Keep a late path: when the server says an action was special and the client
  had not been told, show it on the server's word.
- Draw from a stream of its own, and give tests a switch for the chance:
  every existing test that counts an exact effect turns flaky at the
  feature's rate the day it ships.
- Related: [[prediction-until-next-update-ends-on-a-stale-update]],
  [[shared-rng-couples-unrelated-agents]].
