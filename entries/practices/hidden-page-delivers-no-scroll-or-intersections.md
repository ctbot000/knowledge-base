---
title: A hidden page delivers no scroll events and no IntersectionObserver entries, so scroll-revealed content never appears
tags: [browser, dom, frontend]
added: 2026-09-19
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver
---

## Fact

While `document.visibilityState` is `hidden`, the page is given neither scroll
events nor observer callbacks. Scrolling it programmatically still moves
`window.scrollY`, and `getBoundingClientRect()` still reports the new geometry —
but a listener registered a moment earlier receives nothing, and an
`IntersectionObserver` watching an element now sitting in the viewport never
fires.

That is fatal to the standard reveal-on-scroll pattern, where content starts at
`opacity: 0` and an observer adds the class that fades it in. The class is never
added, so the page renders blank where its content is.

Even in a visible page the entry is not guaranteed: an observer reports the
intersection state at delivery time, not every transition it passed through. A
fast or programmatic scroll can deliver `isIntersecting: false` for an element
that crossed the viewport between frames, and a one-shot reveal skips it.

## Why it matters

It fails exactly where it cannot be seen: a link opened in a background tab, an
embedded or collapsed pane, a screenshot pipeline, an automated check. Probing
the DOM says the elements exist and the scroll position is right, which sends
you to look at the observer options rather than at visibility.

## How to apply

- Never let an observer be the only thing that can reveal content. Keep a sweep
  that shows anything currently within the viewport, and call it from the scroll
  handler and from `visibilitychange`.
- Treat `visibilitychange` as the catch-up point in general: nav highlighting,
  progress bars and anything else driven by scroll is stale until it fires.
- Scope the initial `opacity: 0` to a class the page's own script adds
  (`html.js .reveal`), so a script that never runs leaves the content visible
  rather than invisible.
- Related throttling: [[hidden-page-timer-budget]],
  [[one-time-build-inside-raf]], [[animation-lifetime-in-frames]].
