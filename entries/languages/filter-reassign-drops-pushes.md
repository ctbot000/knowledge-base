---
title: Reassigning an array to its own filter() loses whatever a callback pushed onto it
tags: [javascript, arrays, game-loop]
added: 2026-11-08
sources:
  - https://tc39.es/ecma262/#sec-array.prototype.filter
---

## Fact

`list = list.filter((x) => x.update(dt))` drops anything an `update` pushes onto
`list` during that call. `filter` fixes its range at the length the array had
when it started, so the new element is never visited and never copied into the
result, and the assignment then discards the old array with the element in it.
Nothing throws.

## Why it matters

It is the usual way to run and prune a list of effects, particles or timers each
frame, and it works until one item starts another as it ends: a shell that
bursts into sparks, a projectile that strikes as it lands. The new item has
already put itself in the scene, so it shows, but it is on no list, so it is
never updated or removed and stays frozen on screen. It looks like a rendering
bug, not a list bug.

## How to apply

Swap in a fresh list before iterating, and keep what lands on it:

```js
const going = this.effects;
this.effects = [];
this.effects = going.filter((f) => f.update(dt)).concat(this.effects);
```

Items added during the pass get their first update on the next frame.
`forEach` over the same array keeps an appended item, so the loss needs both
`filter` and the reassignment. A test that checks nothing is left in the scene
after an effect's lifetime catches it; one that only checks it started does not.
