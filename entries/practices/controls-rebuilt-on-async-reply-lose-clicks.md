---
title: Controls rebuilt when an async reply arrives lose the click that lands in between
tags: [ui, dom, async, testing]
added: 2026-10-04
---

## Fact

A view that draws its own buttons (tabs, filters) in the same `render()` it
calls when fetched data arrives replaces those buttons under the user. A press
that starts on the old node and ends after the swap, or a click aimed at a node
that was just removed, reaches nothing: no handler runs and no error is thrown.

## Why it matters

The window is the network round trip after opening the view, which is exactly
when people tap a tab. By hand it looks like a tap that "didn't take"; in
browser automation it fails intermittently as `Node is detached from document`
(Puppeteer) or a stale element reference (Selenium), which reads as a flaky
test rather than a bug in the view.

## How to apply

- Build the controls once, when the view opens, and keep references to them.
  A render only updates their state (`classList.toggle('on', ...)`,
  `disabled`, `aria-pressed`) and replaces the data region beside them.
- Re-rendering a control is fine when the user's own action caused it; what
  breaks is a redraw triggered by something the user did not do, such as a
  reply, a timer or a push.
- A test that clicks a control right after opening a view that fetches is the
  cheapest check: it fails on the detached node whenever the reply wins.
