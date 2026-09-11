---
title: AudioContext.currentTime is the time being handed to the output, not the time being heard
tags: [web-audio, audio, frontend]
added: 2026-09-11
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/outputLatency
---

## Fact

A sample scheduled at audio time `T` becomes audible at roughly
`T + ctx.outputLatency`, because `currentTime` advances with the buffer being
passed to the host audio system, not with the speaker. The gap is a few
milliseconds on a wired output and tens of milliseconds over Bluetooth or a
shared device.

Anything drawn from `currentTime` is therefore drawn that far ahead of the
sound it belongs to:

```js
const audible = ctx.currentTime - (ctx.outputLatency || ctx.baseLatency || 0);
```

## Why it matters

Audio and visuals both derive from the same clock, so they look consistent in
code and in every log; only a human watching them disagrees. It reads as "the
animation feels slightly early", which gets chased into easing curves and frame
scheduling rather than into the clock.

The error is a constant offset per output device, so it survives every test on
the developer's machine and appears when a user plugs in headphones.

## How to apply

- Subtract the latency once, in the single function that converts
  `currentTime` into your own timeline, and read every visual from that.
- `outputLatency` is not implemented everywhere; fall back to `baseLatency`,
  which reports only the context's own buffering and is a lower bound, and clamp
  the result to a sane range before trusting it.
- Read it per call rather than caching: it is 0 before playback begins and can
  change when the output device does.
