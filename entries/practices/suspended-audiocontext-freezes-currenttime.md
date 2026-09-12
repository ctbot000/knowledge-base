---
title: A suspended AudioContext holds currentTime still, so any clock derived from it stops
tags: [web-audio, audio, browser]
added: 2026-09-12
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/currentTime
  - https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/resume
---

## Fact

`AudioContext.currentTime` advances only while the context's state is
`running`. A context constructed before any user gesture starts `suspended`
under the autoplay policy, and a browser may suspend a running one again when
the page is backgrounded or the output device changes.

While suspended it does not throw, reset, or report anything unusual: it holds
whatever finite, non-zero value it had reached. Anything clocked on it —
playback position, progress, a whole simulation — therefore stops dead while
rendering carries on at full frame rate.

`resume()` returns a promise that settles only once the context is actually
allowed to run, and a `resume()` that is not reached synchronously from a user
gesture handler may never settle at all.

## Why it matters

The frozen value looks exactly like a working clock. It is finite, it is not
zero, and reading it twice inside one frame legitimately returns the same number
even on a healthy context, so the obvious sanity checks pass.

The symptom is "everything draws, nothing moves", which points at the frame loop
or at the update function — neither of which is at fault. It also hides during
development, because interacting with the page to test it is itself the gesture
that resumes the context.

## How to apply

- Treat `state === 'running'` as a precondition of the *clock*, not just of the
  sound. Either gate the start of anything time-driven on it, or carry the time
  forward on a wall clock while suspended, anchored so it cannot jump:

  ```js
  if (ctx && ctx.state === 'running') {
    anchorAudio = ctx.currentTime;
    anchorPerf = performance.now() / 1000;
    return anchorAudio;
  }
  return anchorAudio + performance.now() / 1000 - anchorPerf;
  ```

- Call `resume()` from inside the gesture handler, not from a timer or a
  continuation after an `await`.
- Listen for the context's `statechange` event rather than polling `state`.
- When nothing is moving, separate the two candidates before debugging either:
  log `ctx.state` **and** a `requestAnimationFrame` counter. A hidden surface
  delivering no frames and a frozen audio clock present identically.

Related: [[audiocontext-currenttime-is-not-audible-time]],
[[hidden-surface-delivers-no-frames]].
