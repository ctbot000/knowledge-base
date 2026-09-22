---
title: A one-shot entry animation replays every time its element is recreated, so a wholesale re-render turns it into a flicker
tags: [css, animation, frontend]
added: 2026-09-22
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Using_CSS_animations
---

## Fact

A CSS animation belongs to the element, not to the data it is showing. Replacing
a node restarts the animation from the beginning, so a render function that
rebuilds a subtree from state replays every entry animation inside it on every
state change — including changes that have nothing to do with the animated
elements.

The result is not a visible animation. Each replay is cut short by the next
render, so the elements sit permanently in the early frames of the keyframes:
faded, offset, or half-scaled.

## Why it matters

It reads as a CSS bug — wrong opacity, wrong transform, a broken theme — and the
animation is correct. It is also invisible while nothing else is happening, so
it only appears once the surface starts updating often, which is exactly when a
screenshot is hardest to interpret.

## How to apply

- Build each element once and update it in place. Rebuild only the nodes whose
  content actually changed, gated on a signature of that content:

  ```js
  const sig = items.map((i) => i.id).join(',');
  if (sig !== node.dataset.sig) {
    node.dataset.sig = sig;
    node.replaceChildren(...items.map(render));
  }
  ```

- When an animation *should* replay on demand, restart it deliberately: remove
  the class, force a reflow with `void el.offsetWidth`, add it back.
- A framework that keys its children solves this by identity; the trap is the
  hand-written `replaceChildren()` render, which has no identity at all.
