---
title: The async Clipboard API can be denied where execCommand('copy') still works
tags: [clipboard, permissions, browser, frontend]
added: 2026-10-03
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText
  - https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand
  - https://html.spec.whatwg.org/multipage/interaction.html#transient-activation
---

## Fact

`navigator.clipboard.writeText` is gated by a permission that the embedding
browser decides. Embedded views (desktop-app webviews, in-app browsers) can
reject it with `NotAllowedError: Write permission denied` inside a real click,
in a secure context, with `clipboard-write` allowed by permissions policy.

`document.execCommand('copy')` on a selected `<textarea>` is gated only by user
activation, so it still succeeds in that same click — even after awaiting the
rejected `writeText`, because transient activation lasts a few seconds
(verified in Chromium).

## Why it matters

A "Copy" button that only uses the async API works in a normal browser tab and
fails for everyone opening the page inside another app — exactly where links to
shared results tend to be opened.

Neither path works from a script-dispatched `element.click()`, which carries no
activation, so automation reports "copy failed" for both and hides which one
real users would hit. Test with real input.

## How to apply

- Try `writeText` first; on rejection, put the text in an off-screen read-only
  `<textarea>`, `select()` it, call `execCommand('copy')`, remove it, and
  return focus to the button.
- Report failure only when both paths fail.
- Do the fallback in the same click handler; do not defer it behind a timer or
  a second user prompt.
