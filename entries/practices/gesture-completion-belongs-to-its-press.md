---
title: A pointer gesture is completed by the element it started on, not by the one under the release
tags: [dom, events, pointer-events, ui]
added: 2026-09-14
---

## Fact

When one button carries two gestures — drag to move the view, click to act —
the release has to be attributed to where the press began. The natural-looking
guard on the release is wrong:

```js
element.addEventListener('pointerdown', (e) => { press = {...}; });
window.addEventListener('pointerup', (e) => {
  if (e.target !== element) return;      // discards real clicks
  if (!press.moved) act(e);
});
```

`pointerup` is listened for on `window` precisely so a drag that leaves the
element still completes — and then `e.target` is the window, or whatever the
pointer happens to be over. The press record is already the authority: it only
exists because the gesture started on the element.

```js
window.addEventListener('pointerup', (e) => {
  const started = press; press = null;
  if (!started || started.moved) return;
  act(e);
});
```

## Why it matters

It fails as a *dead control* rather than as an error. The drag half of the
pair keeps working, which argues that the listener, the hit region and the
coordinate maths are all fine, so the search goes to the action being
triggered instead of to the guard that never let it run.

An overlay stacked above the element makes the same mistake easy to reach for
from the other direction — `pointer-events: none` is what lets the press
through, and a target check then rejects what the press correctly accepted.

## How to apply

- Record the press on the element; decide on the release from that record.
- Keep a movement threshold (a few pixels) so a click with hand-tremor is
  still a click, and set the flag once rather than per move.
- Track the move and release on `window`, not on the element, or a gesture
  that leaves it never finishes.
- Verify by dispatching the release somewhere else on purpose — at the window,
  or over a sibling — and asserting the action still fires.

Related: [[setpointercapture-throws-for-inactive-pointer-id]], [[element-click-does-not-hit-test]].
