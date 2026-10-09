---
title: A timer that steps a fixed dt per tick falls behind a wall-clock simulation when the event loop lags
tags: [simulation, game-loop, testing, node]
added: 2026-10-09
---

## Fact

`setInterval(() => step(TICK_MS / 1000), TICK_MS)` assumes every tick fires on
time. Under load ticks fire late or are dropped, so that body moves at a
fraction of real speed, while anything stepping by elapsed time
(`now - lastTick`) keeps full speed. Two such loops sharing one world drift
apart exactly when the machine is busy.

## Why it matters

A bot or AI player chasing server-simulated monsters, a client-side predictor
against an authoritative server, or a test fixture against the system under
test: each passes alone and flakes only under full-suite or production load.
Side effects follow (stuck detection on wall-clock time fires, the bot changes
mode), so the failure looks like logic, not timing.

## How to apply

- Step every loop that shares a world by elapsed time, capped
  (`dt = min(0.25, (now - last) / 1000)`), and let the physics substep it.
- Reproduce load flakes by lagging the event loop on purpose instead of hogging
  CPUs (which starves the whole run): in the test, add
  `setInterval(() => { const e = Date.now() + 60; while (Date.now() < e); }, 80)`.
  A timing bug then fails nearly every run, and the fix can be shown to hold.
