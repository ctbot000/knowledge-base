---
title: HTMLImageElement.decode() never settles on a page that is not being painted
tags: [browser, dom, async]
added: 2026-09-20
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/decode
---

## Fact

`await img.decode()` on a hidden, backgrounded or occluded page returns a
promise that stays pending indefinitely. It does not reject and it does not
time out.

The image itself is fine. Measured on a hidden page, with a data-URL PNG:

```
document.hidden        true
img.complete           true      <- fully loaded
img.naturalWidth       64        <- fully loaded
onload                 fires immediately
img.decode()           still pending at 5.7s
createImageBitmap()    resolves immediately, 64x64
```

Forcing a single paint resolved the pending promise at once, with
`document.hidden` still `true` — so the gate is the paint, not the visibility
flag. `decode()` promises *paint readiness*, which is precisely what a page
that is not painting never reaches.

## Why it matters

It is an `await` that never returns and never throws, so everything downstream
is simply absent with no error anywhere. Nothing logs, nothing rejects, no
request fails.

The obvious diagnosis — "the image did not load" — is contradicted by
`complete === true` and a real `naturalWidth`, which sends the search somewhere
else. And it is invisible in development, where the window under test is
focused; it appears in a background tab, an off-screen iframe, a headless or
automated browser, and any pane the host app has collapsed.

## How to apply

- For anything that must finish off-screen, decode with
  `createImageBitmap(blob)` or just wait for `load`. Neither is paint-gated.
- Keep `decode()` only for what it is for: holding an element out of the DOM
  until inserting it cannot flash. Race it with a timeout if it sits on a
  critical path.
- Suspect it whenever an async pipeline stalls with no error and the page is
  not on screen.

Related: [[hidden-page-timer-budget]],
[[hidden-page-delivers-no-scroll-or-intersections]],
[[one-time-build-inside-raf]].
