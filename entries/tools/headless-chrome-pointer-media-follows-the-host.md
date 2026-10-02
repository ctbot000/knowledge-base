---
title: Headless Chrome answers pointer and hover media queries from the machine's own input devices
tags: [testing, automation, browser, puppeteer, ci]
added: 2026-10-02
sources:
  - https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#method-setEmulatedMedia
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/any-pointer
---

## Fact

`pointer`, `any-pointer`, `hover` and `any-hover` are not emulated by default,
so headless Chrome evaluates them against whatever input devices the machine
running it has. A laptop with a trackpad matches `(any-pointer: fine)`, and a
CI runner with no mouse does not. `Emulation.setEmulatedMedia` silently
ignores these four features: no error, and nothing changes. Touch emulation
(Puppeteer's `hasTouch: true`) does change them, but only towards touch:
`pointer: coarse`, `hover: none`, no fine pointer.

## Why it matters

A page that switches to touch controls when there is no fine pointer is
tested in two different modes by the same suite. On the laptop the touch-only
controls stay `display: none`, so a layout test passes there and fails in CI
on the first change that moves them. It reads as a CI flake or a font
difference between platforms, but the CI result is the one that is true for
touch screens.

## How to apply

- Set the mode in each test rather than inheriting it from the host:
  `hasTouch: true` for touch. No setting forces a fine pointer, so for mouse
  runs stub the app's own check (for example `matchMedia` in an init script)
  or accept that CI will run that test in touch mode.
- Before blaming CI for a layout failure that does not reproduce, run the
  suite locally in touch mode too.
- Log `matchMedia('(any-pointer: fine)').matches` in CI once, to know which
  mode it runs.
