---
title: UI synced only from the animation loop cannot render the state change that stopped the loop
tags: [browser, requestAnimationFrame, ui]
added: 2026-09-09
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
---

## Fact

A common structure keeps one source of truth and reflects it into the DOM once
per frame: the click handler mutates state, and the `requestAnimationFrame`
callback pushes score, panels and buttons out to the page. It works perfectly at
60 Hz.

It fails wherever frames are scarce — a backgrounded or occluded window, a
low-power mode, an embedded or snapshotting renderer — because the mutation
lands immediately and its visible consequence waits for a frame that is not
coming. The sharpest case is self-inflicted: a `visibilitychange` handler that
pauses on hide and shows a "Paused" panel from the loop can never paint that
panel, because becoming hidden is exactly what stopped the frames.

## Why it matters

The state is correct, so nothing looks broken from the inside — a probe of the
model reports `paused`, while the DOM still says `playing` and the panel is
still `hidden`. The gap is invisible to any check that reads state rather than
the rendered page, and it reads as a stuck button rather than as a timing
structure.

It also hides in development, where the window under test is always focused and
frames are plentiful.

## How to apply

- Push to the DOM synchronously from the handler that changed the state, in
  addition to the per-frame sync: wrap the mutation, `act(fn) { fn(); sync(); }`.
- Reserve the frame loop for what genuinely changes every frame — a timer
  readout, a meter — and treat discrete state transitions as event-driven.
- Never place a visibility- or focus-triggered UI change on the loop; that path
  is throttled by definition.
- Verify by asserting on rendered DOM after dispatching the event, not on the
  model the handler wrote to.

Related: [[animation-lifetime-in-frames]], [[hidden-surface-delivers-no-frames]].
