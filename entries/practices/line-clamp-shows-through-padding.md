---
title: A -webkit-line-clamp box with vertical padding shows the top of the first hidden line
tags: [css, typography, overflow]
added: 2026-10-02
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-line-clamp
---

## Fact

`display: -webkit-box; -webkit-line-clamp: N; overflow: hidden` only makes the
box N lines tall. The lines after the Nth are still laid out and painted below
them, and `overflow: hidden` clips at the padding edge, so the bottom padding
is a window onto the first hidden line, cut through its letters. Seen in
Chrome 154.

## Why it matters

The defect shows only when the text is long enough to be clamped, which is
exactly when the ellipsis was meant to make it tidy. A pill or card tested with
short strings looks right; a real long message hangs a sliver of text under
the ellipsis.

## How to apply

- Keep the vertical space out of the clip: a transparent border instead of
  padding (`border: solid transparent; border-width: 7px 12px;`; the background
  still paints under a border by default), or padding on a wrapper element.
- Test a clamped element with text at least one line longer than the clamp.
