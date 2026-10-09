---
title: A Puppeteer Ctrl+V or Cmd+V pastes nothing; the key must carry the Paste command
tags: [testing, automation, puppeteer, clipboard, cdp]
added: 2026-10-09
sources:
  - https://pptr.dev/api/puppeteer.keyboarddownoptions
---

## Fact

Keys sent through CDP (Puppeteer's `page.keyboard`) do not run the browser's
editing shortcuts. In headless Chrome, `Meta`+`V` or `Control`+`V` into a focused
input leaves it empty, even with clipboard permissions granted and text on the
clipboard. `keyboard.press('KeyV', { commands: ['Paste'] })` pastes. The same
holds for `Copy`, `Cut`, `SelectAll` and `Undo`. `ControlOrMeta` is a Playwright
key name; Puppeteer throws `Unknown key`.

## Why it matters

A copy-and-paste test written with a modifier chord fails as if the app's
paste were broken, or passes for the wrong reason when it only checks the
clipboard.

## How to apply

```js
await page.browserContext().overridePermissions(origin, ['clipboard-read', 'clipboard-write', 'clipboard-sanitized-write']);
await page.focus('input');
await page.keyboard.press('KeyV', { commands: ['Paste'] });
```

Read the clipboard back with `navigator.clipboard.readText()` inside the page,
with the page in front (`bringToFront()`), since an unfocused document is refused.
Seen with Puppeteer 25 and Chrome 154.
