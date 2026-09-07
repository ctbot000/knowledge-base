---
title: A lifecycle autosave persists the placeholder state behind the menu
tags: [persistence, ui, browser]
added: 2026-09-08
---

## Fact

Menus commonly render over a live but inert instance of the thing they launch —
a demo world behind a title card, a blank document behind a template picker.
That instance is indistinguishable from a real one at the persistence layer.

So an autosave wired to a lifecycle event fires for it:

```js
window.addEventListener('beforeunload', save);   // runs even if nothing started
```

Merely opening the page and leaving writes a save. On the next visit the menu
offers "Continue" for a session the user never began, restoring a placeholder as
if it were their progress.

## Why it matters

It only appears on a clean profile, which is the one state the developer never
has. Local storage from testing hides it completely, and by the time the entry
point is reviewed the save has existed for weeks.

The failure is also self-confirming: the offer looks correct, because a save
genuinely exists.

## How to apply

- Guard persistence on an explicit **session-started** flag, set where the user
  actually commits, and check it inside the save function rather than at each
  call site — lifecycle handlers are easy to forget.
- Do not guard on "state exists". Placeholder state exists too.
- Verify on a clean profile: load the entry point, navigate away, come back, and
  assert the resume affordance is absent.
