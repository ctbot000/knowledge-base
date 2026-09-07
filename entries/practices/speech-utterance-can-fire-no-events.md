---
title: A speech utterance that never starts also never ends, while speechSynthesis.speaking reads true
tags: [web-speech, browser, async, frontend]
added: 2026-09-07
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/speaking
  - https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/start_event
---

## Fact

`speechSynthesis.speak(u)` flips `speechSynthesis.speaking` to `true`
synchronously, before any audio exists. If the utterance can then never start —
the page has not been interacted with and autoplay policy blocks audio, or the
surface renders no sound — the browser neither starts it nor rejects it.
`onstart`, `onend` and `onerror` all stay silent indefinitely.

Measured in a Chromium surface with 180 voices installed: 24 seconds, zero
events, `speaking === true` and `pending === false` on every sample. The
utterance is not queued and not failed; it is simply never spoken.

## Why it matters

The idiomatic wrapper resolves a promise from `onend` and `onerror`, so that
promise never settles and every `await speak(...)` deadlocks the state machine
around it. The interface stays in its "speaking" state forever, with no error
anywhere to explain it.

Both obvious health probes agree that nothing is wrong: `speaking` is `true`
and `pending` is `false`, which is exactly what a healthy in-progress
utterance looks like. So the stall reads as an application bug rather than a
swallowed utterance.

## How to apply

- Never settle a `speak()` promise on `onend`/`onerror` alone. Add a wall-clock
  watchdog sized from the text, e.g. `4000 + words * 620 / rate` ms.
- Treat "no `onstart` within ~1.5 s" as the real signal that nothing is
  playing; `speaking === true` is not evidence of audio.
- Set a flag inside `onstart` and use *that* to decide whether the listener
  actually heard anything.
- The usual cause is the autoplay gesture requirement, so re-speak the first
  utterance on the first `pointerdown`/`keydown` rather than staying silent.
