---
title: Node's strict assertions fail -0 against 0
tags: [javascript, testing, numerics]
added: 2026-09-07
updated: 2026-09-14
sources:
  - https://nodejs.org/api/assert.html#assertstrictequalactual-expected-message
---

## Fact

`assert.strictEqual`, and `assert.equal` from `node:assert/strict`, compare with
`Object.is`, which distinguishes negative zero from positive zero. `===` does
not. So this passes and that throws, on the same two values:

```js
-0 === 0;                 // true
Object.is(-0, 0);         // false
assert.strictEqual(-0, 0) // AssertionError:  + -0  - 0
```

`-0` arrives from ordinary sign-flipping code — `return white ? score : -score`
returns `-0` whenever the score is zero, as does `-(0)`, `0 * -1`, and
`Math.round(-0.2)`.

It also arrives from plain arithmetic with no sign flip in sight. Any multiply
or divide that lands on zero with an odd number of negative operands gives `-0`,
so `0 / -4` and Cramer's rule over a matrix with a negative determinant both
produce it. A solver that returns a vector of small integers can hand back
`[2, -0, -2]`, which then fails `deepEqual` against the `[2, 0, -2]` it was
checked against.

## Why it matters

The failure message reads as a rendering bug in the test runner: expected `0`,
got `-0`, which look like the same number and print the same everywhere else.
`console.log` shows `-0` but `JSON.stringify(-0)` is `"0"` and string
interpolation gives `"0"`, so the usual ways of inspecting the value all hide the
thing that is failing.

It bites hardest on symmetric functions that are asserted to be zero: an
evaluation that negates for one side, a balance that nets out, a delta between
equal readings, a linear solve where one unknown comes out unused. Those are
exactly the cases a test suite checks against zero.

`assert.deepEqual` from `node:assert/strict` compares leaves the same way, so a
single `-0` anywhere in an array or object fails the whole comparison — and the
printed diff shows `+ -0` against `- 0`, one character apart.

## How to apply

- Compare the magnitude when a sign flip can produce it: `assert.equal(Math.abs(x), 0)`.
- Normalise at the exit of anything that computes numbers rather than at each
  assertion: `n === 0 ? 0 : n` on the way out of a solver costs nothing and
  means callers never have to know.
- Or normalise the value where it is produced. `x + 0` converts `-0` to `+0`
  (`Math.abs` and `x || 0` do too); `-x` does not.
- Do not "fix" it by switching the assertion to `assert.ok(a === b)`. That hides
  the distinction rather than deciding about it, and loses the diff on failure.
- Keep `-0` deliberately only when the sign carries meaning — direction of
  approach to zero, or a value fed to `Math.atan2` or `1/x`, where it changes the
  result.
