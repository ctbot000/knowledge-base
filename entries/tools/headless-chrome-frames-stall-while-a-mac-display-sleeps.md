---
title: Headless Chrome on a Mac delivers almost no animation frames while the display is asleep
tags: [testing, automation, browser, headless, macos]
added: 2026-11-12
---

## Fact

On a Mac whose display has gone to sleep (nobody at the keyboard), pages in
headless Chrome still load, run timers, take clicks and play video, but
`requestAnimationFrame` nearly stops. The pages are not hidden:
`document.hidden` is false. Seen with Chrome 157 in the new headless mode with
GPU rendering (ANGLE on Metal) on an Apple Silicon laptop: a frame-driven test
that takes 6 seconds took 17 minutes, while a test that only waits on the DOM
passed in its usual 3 seconds. Waking the display restored normal speed at
once.

## Why it matters

An unattended run (a pre-push hook, a scheduled job, an agent working while the
user is away) fails with timeouts scattered over unrelated tests, an hour
later. It looks like a flaky suite or a broken change, and the tests that
never wait on a frame still pass, which points away from the machine. Run
again with someone at the keyboard, everything passes.

## How to apply

- Hold the display awake for the run: `caffeinate -d -u <command>`. `-u`
  declares user activity, which wakes a sleeping display; `-d` keeps it from
  sleeping until the command exits. Nothing is changed for good.
- When a browser suite times out all over, check the display before the code:
  `pmset -g assertions | grep UserIsActive` reads `0` while the user is idle.
- The tell is which tests are slow: only those that wait for the page's own
  loop to advance. See also [[hidden-surface-delivers-no-frames]], the same
  starvation from a hidden document.
