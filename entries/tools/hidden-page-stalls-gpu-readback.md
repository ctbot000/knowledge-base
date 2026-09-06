---
title: A hidden page stalls asynchronous GPU readback, which silently inverts benchmark results
tags: [testing, automation, browser, webgl, benchmarking]
added: 2026-09-06
---

## Fact

In a document reporting `document.hidden === true` — a background tab or an
automation pane — `requestAnimationFrame` never fires, and WebGL readback that
resolves asynchronously stalls with it. Measured on TensorFlow.js with the WebGL
backend: the first `tensor.data()` after a GPU op took ~35 s, while `dataSync()`
on an equivalent tensor returned in ~50 ms. Every later async read cost a flat
~2 s, unchanged whether the work was a 320- or a 416-pixel input.

Synchronous readback is unaffected, so the stall follows the *readback style*,
not the amount of computation. Nothing in the stalling code refers to animation
frames, so nothing in a stack trace points at the cause.

## Why it matters

The symptom is one code path that is inexplicably slow while a sibling path is
fast, and the ranking of two implementations can come out backwards. A
lightweight object detector timed tens of times *slower* than the heavyweight
one it should beat, purely because its post-processing read back
asynchronously — an entirely correct result for the surface, and entirely wrong
about the code. Any optimisation, default, or "obviously the fast one" decision
made on those numbers is inverted.

A flat constant is the tell: real GPU work scales with input size, a stalled
poll does not.

## How to apply

- Check `document.hidden` before trusting any GPU timing, and treat a duration
  that does not move with input size as measurement, not computation.
- Time the same tensor through a sync read as a control. If only the async path
  is slow, the surface is at fault, not the code.
- Benchmark GPU work in a visible window; use a hidden surface for correctness
  assertions read out of the DOM, not for performance.
- The frame starvation behind this is [[hidden-surface-delivers-no-frames]];
  what it does to screenshots is [[screenshot-lags-committed-dom-state]].
