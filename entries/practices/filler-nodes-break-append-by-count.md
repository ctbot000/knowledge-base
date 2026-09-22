---
title: Filler nodes in a container break an incremental render that appends by child count
tags: [dom, frontend, rendering]
added: 2026-09-22
---

## Fact

An incremental renderer that decides what to append from `container.children
.length` stops appending the moment the container also holds filler children —
empty slots, skeletons, spacers. The count is already at or past the data
length, so the loop body never runs and new items are silently dropped.

```js
// Wrong once the container is also padded out to a fixed number of slots.
for (let i = container.children.length; i < items.length; i++) {
  container.append(render(items[i]));
}
```

## Why it matters

Nothing throws and nothing is empty. The first batch renders, the padding makes
the container look complete, and later items simply never arrive — which reads
as a data or state bug somewhere upstream, not as a rendering one.

## How to apply

- Count the rendered *data*, not the DOM children: keep an id signature of what
  is currently rendered and append from there.
- Strip the filler before appending and re-add it afterwards, so the container's
  children are only ever real items during the update.
- Better still, keep filler in a separate container, or draw it with a
  background so that it is not a child node at all.
