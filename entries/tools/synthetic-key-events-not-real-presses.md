---
title: Synthetic key events do not trigger the native activation a real key press does
tags: [testing, automation, dom, keyboard]
added: 2026-08-29
updated: 2026-09-12
sources:
  - https://dom.spec.whatwg.org/#trusted-events
  - https://developer.mozilla.org/en-US/docs/Web/API/Event/isTrusted
---

## Fact

A keyboard event injected by test or agent tooling is not equivalent to a key
press. Events built with `new KeyboardEvent(...)` are untrusted (`isTrusted`
false) and by specification run no default action, so Enter on a focused
`<button>` dispatches the listener but never produces the `click`. Driver-level
injection (CDP `Input.dispatchKeyEvent` and friends) is trusted but only as
faithful as its parameters: harnesses routinely send a keydown with no `key`
value at all, which arrives as `e.key === ""`.

The usual cause is a key *name* the driver did not recognise. Tools that take a
key by name map the DOM key values, so the legacy aliases fail silently —
`Return` and `Left` dispatch a trusted event carrying `key: ""` while `Enter` and
`ArrowLeft` work. No error is raised; the tool reports the press as sent.

## Why it matters

It splits the UI into behaviour that works for people and behaviour that works
under automation, in both directions. A confirm step wired to a focused button's
native activation looks broken in every automated run while being fine in
production. Worse is the reverse: the automation "passes" against a handler that
matches on `e.key`, so nobody notices that the app never saw the key it thought
it did.

Debugging goes badly because the symptom — a keypress doing nothing — points at
application state, focus, or event ordering, none of which are the cause.

## How to apply

- Before blaming the app, log what actually arrived:
  `addEventListener('keydown', e => console.log(e.key, e.code, e.isTrusted), true)`.
  An empty `key` or `isTrusted: false` identifies the harness, not a bug.
- Do not route a state transition solely through a control's native activation.
  Handle the key explicitly and let the guard on the state make a duplicate
  native `click` a no-op.
- Send the DOM key value, not its alias: `Enter`, `ArrowLeft`, `Escape`,
  `Backspace`. This is the fix in most cases, and it is cheaper than changing the
  application to accommodate the harness.
- `e.code` is worth matching for layout independence, but it is not a reliable
  fallback, and it fails in both directions: an injection that drops `key` often
  drops `code` with it, while a driver that takes a *character* rather than a key
  name sends the mirror image — `key: "e"` with `code: ""` — which silently
  defeats a handler matching on `code` alone. Accept either, deriving a code from
  `key` when `code` is empty.
- Assert keyboard paths through the application's own state, not through the
  rendered result of a native default action.
