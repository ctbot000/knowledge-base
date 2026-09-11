---
title: Stubbing requestAnimationFrame to freeze an app also freezes the surface that captures it
tags: [testing, automation, browser, requestAnimationFrame]
added: 2026-09-11
---

## Fact

Replacing `window.requestAnimationFrame` with a no-op is the obvious way to
hold a running app still for a screenshot: the loop stops re-registering, and
nothing advances. It works — and it also stops the screenshot.

Automation surfaces drive their capture through the same frame pipeline. With
the callback neutralised, the returned image is whatever was last painted,
which can be seconds or whole state transitions old. The app is correct, the
surface is visible, and the picture is a different program.

The tell is a disagreement in one direction only: the DOM and the canvas both
report the new state, the image reports the old one. Reading a pixel back with
`getImageData` confirms the canvas holds the new frame while the capture does
not.

## Why it matters

It is self-inflicted and it arrives exactly when the evidence matters most —
at the point of recording a result. The image looks like a real observation, so
a composed scene that never happened gets accepted, and a change that did land
gets "confirmed" as broken.

It also mimics an app bug convincingly. A stale capture showing a panel that
the model says is closed reads as a UI sync fault, which sends the work into
event wiring that is fine.

## How to apply

- Freeze the **simulation**, not the frame loop: zero the rates the world moves
  by (speed, spawn timers, drift) and let the real loop keep painting the same
  state. Re-apply on an interval if the app resets them.
- If the loop must be stopped, verify against the DOM and `getImageData` rather
  than the returned image, and restore the real function before capturing.
- Treat any image taken while you were holding the app still as unconfirmed
  until one non-image read agrees with it.

Related: [[screenshot-lags-committed-dom-state]], [[hidden-surface-delivers-no-frames]].
