---
title: element.click() proves the handler runs, not that anything can reach the control
tags: [testing, automation, dom]
added: 2026-09-14
---

## Fact

`el.click()` — and any `dispatchEvent(new MouseEvent('click'))` — invokes the
event path on that node directly. It performs no hit test, so it never asks the
question a real pointer asks: *what is actually on top of this point?*

A control can therefore be completely unreachable — covered by an overlay,
inside a `pointer-events: none` subtree, behind a transformed ancestor, scrolled
out of view, zero-sized — and a suite driving it this way passes every time.

Driver-level clicks (CDP `Input.dispatchMouseEvent`, a real automation click at
coordinates) do hit-test, which is why the same test written two ways can
disagree.

## Why it matters

It is a false pass on the one thing a UI test exists to establish. The coverage
number goes up, the interaction is "tested", and the feature is dead for every
human who opens it. Because the handler genuinely works, reproducing the report
by calling the same code confirms the wrong conclusion — the bug is not in
anything the test touches.

It hides exactly the regressions that are easiest to introduce and hardest to
spot by reading a diff: a new overlay, a `pointer-events` change, a stacking or
transform context that moved.

## How to apply

- Assert reachability separately from behaviour, and cheaply: for each control,
  `document.elementFromPoint(cx, cy)` must resolve to it or to something inside
  it. One pass over the interactive elements of a page catches the whole class.
- Prefer a driver click over `el.click()` whenever the point of the test is that
  a person can use the thing.
- Be suspicious of any test that passes on markup you have never pointed at with
  a real cursor.
- `isTrusted` is a different axis of the same problem; see
  [[synthetic-key-events-not-real-presses]].
