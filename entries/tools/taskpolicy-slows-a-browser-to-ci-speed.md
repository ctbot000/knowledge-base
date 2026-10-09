---
title: On an Apple Silicon Mac, taskpolicy -c background slows a whole browser to CI speed, where CDP CPU throttling misses the GPU process
tags: [testing, automation, ci, macos, browser]
added: 2026-10-02
sources:
  - https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#method-setCPUThrottlingRate
---

## Fact

`taskpolicy -c background <command>` runs a command under the background QoS
clamp, which keeps its threads on the efficiency cores, and every process it
starts inherits the clamp (`man taskpolicy`). Put in front of a test command, it
slows the browser's renderer and GPU processes alike: a headless-Chrome test
with software rendering went from 6 s to 27 s, inside the 15-48 s it takes on a
CI runner, and failed the same way CI did. CDP's
`Emulation.setCPUThrottlingRate` slows only the renderer's main thread, so a
page whose time goes to software rendering in the GPU process barely slows.

## Why it matters

Timing bugs that only show with CI's slow software rendering, such as frames
seconds apart or a press landing while a dialog still animates, never show on a
fast laptop, and the obvious throttle leaves the slow part untouched. Without a
reproduction a fix is a guess, checked by pushing it.

## How to apply

- Prefix the suite's own command, with whatever makes it render in software as
  CI does: `CI=1 taskpolicy -c background npm test`.
- The clamp can also wedge a run outright rather than slow it: with the
  browser on a real GPU (metal) and the desktop's own browser busy with it, a
  whole suite under `taskpolicy -c background` sat at 0% CPU for many minutes
  with every Chrome process idle — background QoS never got GPU work
  scheduled. When the run must use the real GPU, or the machine is busy, leave
  the default QoS and accept the faster, less CI-like timing.
- Loop the flaky test under it and count failures before and after a fix.
- Instrument the page in those runs (gaps between animation frames, what each
  press hit, the app's own state) instead of reasoning from the CI log.
- What it typically uncovers: [[stepped-frames-leave-a-software-gpu-behind]],
  [[puppeteer-click-aims-before-it-lands]].
