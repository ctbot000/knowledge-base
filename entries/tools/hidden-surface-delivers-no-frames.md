---
title: An automation surface that is hidden delivers no animation frames, so a rAF-driven app cannot be driven through it
tags: [testing, automation, browser, frontend]
added: 2026-09-05
---

## Fact

Browser automation panes, headless surfaces and background tabs report
`document.hidden === true`, and a hidden document is throttled until
`requestAnimationFrame` stops firing altogether. Any app whose state advances
inside its rAF loop is therefore frozen for the whole session: input is
accepted, the state machine never runs, and clocks stop.

Screenshots still return an image, because a capture forces a paint of whatever
was last committed. So the surface looks alive while nothing is simulating, and
the state you read back is whatever it was when the pane went hidden.

The tell is an internal clock that will not move: sample the app's own
accumulated time twice across a real delay, and it reads identical.

## Why it matters

Every conclusion drawn this way is wrong in the same direction — the feature
looks broken because the loop never ran. Time then goes into debugging input
handling, event wiring or state transitions that are all correct, and the "fix"
is validated against the next equally frozen run.

`innerWidth`/`innerHeight` can also read `0` on a hidden pane, which quietly
satisfies `(orientation: portrait)` and any `max-width` query, so layout probes
taken there report a device shape that does not exist.

## How to apply

- Check `document.hidden` before concluding anything about a running loop.
- Expose a deterministic step for automation — a function that runs N fixed
  timesteps of update and then draws once. Driving that is faster and more
  reproducible than waiting on real frames, and it makes the whole run seedable.
- Remove the hook before shipping, or gate it behind an explicit flag.
- Read state from the app, not from the picture; see
  [[screenshot-lags-committed-dom-state]]. The same throttling seen from inside
  the app is [[animation-lifetime-in-frames]].
