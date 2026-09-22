---
title: A node cloned into the page for an animation is still matched by the selector that produced it
tags: [dom, animation, frontend]
added: 2026-09-22
---

## Fact

The usual way to fly an element somewhere — clone it, position the clone
absolutely, animate the clone, drop it — leaves a node in the document carrying
every class the original had. The next run of the same effect selects the
originals *and* the clones still in flight, and clones those too. Each run
multiplies, so a surface that animates once per user action ends up with
hundreds of invisible nodes in `<body>`.

## Why it matters

The clones finish transparent, so nothing looks wrong. What shows up first is a
slow leak — memory, layout cost, and every later `querySelectorAll` on that
class returning more rows than there are real elements, which quietly breaks
logic that counts or iterates them.

## How to apply

- Select from the container the real elements live in, and exclude the flight
  class explicitly:

  ```js
  document.querySelectorAll('.seat .chip-stack:not(.flying)')
  ```

- Sweep leftovers at the start of each run; an animation whose promise never
  settles otherwise leaks forever.
- Strip `id` attributes from a clone. `cloneNode(true)` copies them, and a
  duplicate id makes `getElementById` resolve to whichever came first.
