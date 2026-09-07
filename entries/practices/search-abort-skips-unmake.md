---
title: Aborting a make/unmake search by throwing skips every pending unmake
tags: [algorithms, search, error-handling]
added: 2026-09-07
---

## Fact

Recursive search over a mutable structure is normally written as make, recurse,
unmake:

```js
apply(move);
const score = -search(depth - 1);
undo();
```

If the time limit is enforced by throwing from deep inside the recursion, the
stack unwinds straight past every `undo()` on the way out. The structure is left
exactly as mutated as the deepest node the search reached — not restored, and not
obviously broken either.

## Why it matters

The corruption is silent and delayed. The search still returns its best move from
the previous completed depth, so the abort looks like it worked. The damage shows
up at the *next* use of the same object: legal moves computed from a position
nobody ever played, a move that the caller knows is legal being rejected, an
undo stack that no longer matches the move list.

It also hides during development whenever each search gets a fresh copy of the
state — a worker that rebuilds the position from a FEN or a serialized board
never sees it. The bug only appears once the object is reused, which is usually
in the test suite or in a single-threaded fallback path, long after the search
was written.

## How to apply

- Record the undo-stack depth before searching and wind back to it in the
  handler, rather than trusting the recursion to clean up:

  ```js
  const base = state.history.length;
  try { /* iterative deepening */ }
  catch (e) { while (state.history.length > base) undo(); if (!(e instanceof TimeUp)) throw e; }
  ```

- Or do not throw at all: return a sentinel score and check it at every frame, so
  each `undo()` still runs. Cheaper to reason about, noisier to write.
- Assert the invariant in a test — search a position, then check the serialized
  state is byte-identical to what went in. A time-limited search that is never
  actually interrupted in tests will not reveal this, so force a timeout.
- The same trap applies to any backtracking algorithm that restores shared state
  after the recursive call: constraint solvers, graph colouring, puzzle
  generators, transactional tree walks.
