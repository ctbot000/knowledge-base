---
title: A default deferred to the next frame overwrites the explicit choice made before it fires
tags: [browser, async, ui]
added: 2026-09-21
---

## Fact

Deferring a default so it runs against a settled layout is routine:

```js
function showMap() {
  ...
  if (!state.fitted) requestAnimationFrame(() => { state.fitted = fitAll(); });
}
```

The guard is tested when the callback is *scheduled*, not when it *runs*.
Anything that happens in the gap — the rest of start-up, a deep link, a restored
session, a user click — is applied first and then silently thrown away by the
default that was queued before it.

Start-up is where the two collide, because that is where a generic default and a
specific request are both issued in the same tick:

```js
setViewMode('map');                 // queues the default fit
if (deepLink) openTopic(id);        // applies the specific view, synchronously
                                    // next frame: the queued fit wins
```

Nothing throws. The view is simply the default one, so the deep link, the
restored scroll position or the selected item reads as "not implemented".

## Why it matters

The symptom appears in the feature that was overwritten, never in the scheduler
that overwrote it, so debugging starts in the wrong file. It is also
intermittent by nature: whether the specific action lands before or after the
frame depends on how much start-up work sits between them, so it reproduces on a
cold load and vanishes under a debugger.

Any deferral has this shape — `requestAnimationFrame`, `setTimeout(…, 0)`,
`queueMicrotask`, `requestIdleCallback`, a resolved promise's `.then`.

## How to apply

- Re-test the guard **inside** the callback, not only before scheduling it:
  `requestAnimationFrame(() => { if (!state.fitted) state.fitted = fitAll(); })`.
- Make the specific action set the same flag the default checks, so applying a
  deep link cancels the pending default rather than racing it.
- Otherwise keep a scheduling handle and cancel it (`cancelAnimationFrame`) when
  something more specific takes over.
- Test it the way it breaks: open the deep link as a cold first load, not by
  navigating to it from an already-running page.
- A deferral that must run for a different reason — the surface is not
  measurable yet — is [[one-time-build-inside-raf]] and
  [[zero-measurement-poisons-derived-layout]].
