---
title: Puppeteer's click ignores clickCount, so a triple click needs count
tags: [puppeteer, testing, automation, browser]
added: 2026-11-26
sources:
  - https://pptr.dev/api/puppeteer.mouseclickoptions
---

## Fact

`page.click(sel, { clickCount: 3 })` is a single click. `Mouse.click` reads only
`count` (default 1) and overwrites `clickCount` with it before pressing, so the
old option is dropped without a warning. `{ count: 3 }` performs three clicks
and selects the line. Seen in the source of puppeteer-core 25.

## Why it matters

The usual way to replace a field's contents, triple click then type, appends
instead. The test goes on with the old text in front of the new, and what fails
is whatever the combined text breaks later, far from the click.

## How to apply

- Use `count: 3`, or select through the DOM: `el.select()` in an evaluate, then
  type. Assert the field's value before submitting it.
