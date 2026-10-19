---
title: A dialog that focuses its first box after a timeout can take the focus while the user types in another box
tags: [web, dom, focus, flaky-tests]
added: 2026-10-19
updated: 2026-10-19
---

## Fact

`setTimeout(() => first.focus(), 60)` after building a dialog is a common way to
focus it once it is shown. On a busy device the timer can fire late, after the
user (or a test) has already picked another box and begun typing; the focus
jumps back, and the rest of what is typed lands in the first box — a password
in the username field.

## Why it matters

The form fails in a way that looks like a wrong password or a wrong code. In
browser tests it shows only under load, as a wait for the next message timing
out, and passes every time alone.

The timer need not be badly late. A test driver types about a key a millisecond,
so a 60 ms timer firing a few tens of milliseconds late can land dozens of keys
in, and which box it lands in decides the symptom: a test that fills the form
twice fails at its first wait or at its second, and both are this one bug.

## How to apply

Focus only if nothing in the dialog has the focus yet:

```js
setTimeout(() => { if (!dialog.contains(document.activeElement)) first.focus(); }, 60);
```

To prove it, make the jump happen mid-typing on purpose (focus the first box on
the nth input event of the second) and check the old code fails as the flake did.
