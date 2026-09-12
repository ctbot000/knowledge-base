---
title: A generated-puzzle test that reads the answer key never tests the clue
tags: [testing, puzzles, game-design]
added: 2026-09-12
---

## Fact

The obvious test for a procedurally generated puzzle takes the answer from the
generator and applies it:

```js
const p = buildPuzzle(seed);
assert.ok(submit(p.answer).solved);   // the lock accepts its own key
```

That is all it proves. It says nothing about whether the room ever tells the
player what the key is, so it keeps passing when a clue is dropped, when a text
template stops interpolating, or when generator and clue drift apart.

A test that recovers the answer the way a player does — by parsing it back out
of the rendered clue — fails instead:

```js
const read = readTime(logbookProse(p));   // the words on the page
assert.deepEqual(read, p.clock);          // clue and answer must agree
```

## Why it matters

The bug it catches is the worst kind a puzzle can have: an unsolvable room that
is internally consistent. The generator is right, the state machine is right,
the solver is right, and the player cannot know the answer. Nothing throws,
because no code is wrong — only the flow of information to the player is broken.

It is also what manual play-testing is least able to find, because the developer
already knows the answer. See [[no-guess-puzzle-generation]] for the same
concern one level down, in whether the deductions exist at all.

## How to apply

- Read the surface the player reads — the rendered sentence, the table rows, the
  drawn symbol — and parse the answer out of it.
- Keep the answer key off the test's path to the answer. If it is imported for
  anything but the final comparison, the test has stopped testing the clue.
- Sweep a few hundred seeds: clue faults are usually conditional on a value — a
  plural, a wrap-around hour, a tie in a sort.
- The parser earns its keep even though only the test calls it. It is the
  executable statement of "this clue is readable".
