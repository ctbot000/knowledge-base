---
title: setPointerCapture throws for a pointer id the browser has no active pointer for
tags: [testing, automation, pointer-events, dom]
added: 2026-09-07
sources:
  - https://w3c.github.io/pointerevents/#dom-element-setpointercapture
---

## Fact

`element.setPointerCapture(id)` raises `NotFoundError` unless `id` matches an
*active* pointer. A dispatched `PointerEvent` does not create one, so whether a
synthetic drag survives the call is decided by the number that was picked:

```js
el.dispatchEvent(new PointerEvent('pointerdown', { pointerId: 1 }));    // captures
el.dispatchEvent(new PointerEvent('pointerdown', { pointerId: 9999 })); // NotFoundError
```

`1` works only because it collides with the id the browser already assigns to
the mouse pointer (Chrome does; the value is implementation-defined). Nothing
about the event being synthetic is what decides it.

## Why it matters

The throw happens *inside the application's own handler*, part-way through the
state that handler was setting up. A drag that sets `dragging = true` before
capturing is left flagged as dragging with no start point recorded, and the
matching `pointerup` then acts on stale aim or an undefined origin — a wrong
result rather than a visible failure.

For a test, the consequence is worse than a red run: the suite passes on the
lucky id and the same code is untestable the moment someone writes a two-finger
case with ids 2 and 3, or a framework renumbers them.

## How to apply

- Guard the call. It is a convenience, not a precondition, so failing to capture
  must not abort the gesture:
  `try { el.setPointerCapture(e.pointerId); } catch { /* not capturable */ }`
- Set application state *after* the capture attempt, so a throw cannot leave a
  half-initialised gesture behind.
- Do not read a passing synthetic-pointer test as proof the id is valid; assert
  the handler's own state instead, and vary the id across tests.

Related: [[synthetic-key-events-not-real-presses]].
