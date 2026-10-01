---
title: (display-mode: fullscreen) also matches a tab the user made full screen, so it cannot tell an installed app from a toggled page
tags: [css, pwa, fullscreen, browser]
added: 2026-10-01
sources:
  - https://drafts.csswg.org/mediaqueries-5/#display-modes
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/display-mode
---

## Fact

`@media (display-mode: fullscreen)` matches whenever the page is shown full
screen, however that happened: an installed app launched with
`"display": "fullscreen"`, a `requestFullscreen()` call, or any other way the
browser went full screen. In Chrome it turns true the moment
`document.fullscreenElement` is set and false when it is cleared.

## Why it matters

The common "is this the installed app?" check,
`matchMedia('(display-mode: standalone)').matches || matchMedia('(display-mode: fullscreen)').matches`,
reports an ordinary browser tab as installed as soon as the user presses a full
screen button. Logic built on it misfires at that moment: a full screen toggle
hidden "because the app is already full screen" vanishes exactly when the user
needs it to get back out, and install prompts or app-only layouts switch on in a
plain tab.

## How to apply

- Ask the Fullscreen API first: while `document.fullscreenElement` (Safari:
  `webkitFullscreenElement`) is set, the page is in a toggled full screen, not
  an installed app.
- Detect a Home Screen or installed app with `(display-mode: standalone)`, plus
  `navigator.standalone === true` on iOS; read `(display-mode: fullscreen)` as
  "launched full screen" only while `fullscreenElement` is null.
- For a full screen toggle, skip display-mode entirely: show it whenever
  `document.fullscreenEnabled` is true, and pick "enter" or "exit" from
  `fullscreenElement`.
