---
title: The scaffolding of a CSS 3D scene intercepts the pointer for everything inside it
tags: [css, 3d, pointer-events]
added: 2026-09-14
---

## Fact

A CSS 3D scene needs a few wrapper elements — one to hold the `perspective`,
one or two carrying the rotations. They are almost always full-size flat boxes
sitting at the camera plane, while the things you actually want clicked are
pushed away from the camera by `translateZ`.

Hit testing takes the nearest box, and the nearest box is the scaffolding. So
every click lands on the wrapper:

```js
document.elementFromPoint(x, y)   // → div.world, not the button drawn there
```

Painting is depth-sorted, so the scene looks exactly right. Two other surfaces
join in: a face rotated to sit behind the camera projects to a box many times
the size of the viewport, and a face seen edge-on still covers a wide trapezoid
of screen.

## Why it matters

Nothing errors, nothing looks wrong, and the handler is provably correct when
called directly — so the search starts in the event wiring and the state
machine, which are both fine. A delegated listener makes it worse: the click
does reach the listener, it just arrives with the wrapper as its target, so
`closest('.thing')` returns null and the handler correctly decides to do
nothing.

## How to apply

- `pointer-events: none` on every element that exists only to position the
  scene, then `pointer-events: auto` on the one layer that holds controls.
  Events still bubble through the disabled ancestors, so delegation is fine.
- Let only the surface facing the camera take the pointer. The one behind you
  is both invisible and enormous.
- Verify with `elementFromPoint` at the centre of a control — that is what a
  click follows. Clicking it yourself in devtools is not the same question.
- See [[grouping-property-flattens-preserve-3d]] for the other way these
  wrappers break a scene, and [[element-click-does-not-hit-test]] for why a
  test suite will not notice any of this.
