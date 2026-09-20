---
title: A loop guard counted in iterations silently truncates the request it was meant to protect
tags: [simulation, debugging, api-design]
added: 2026-09-20
---

## Fact

A fixed-step loop that converts a duration into sub-steps is usually written
with a safety counter, to stop a corrupt step size spinning forever:

```js
let remaining = seconds;
let guard = 0;
while (remaining > 1e-6 && guard < 200000) {   // ~14 h at a 0.25 s step
  step(Math.min(MAX_STEP, remaining));
  remaining -= MAX_STEP;
  guard += 1;
}
```

The constant is an implicit limit on the argument. Ask for more than it covers
and the call returns normally, having done part of the work, with no error and
no return value that says so. The caller's clock reads whatever the loop
reached, which is a plausible number.

## Why it matters

Every symptom points away from the guard. The state is self-consistent, just
from an earlier time, so it reads as a model that stops responding, a variable
that "plateaus", or an effect that takes longer to appear than it should. The
threshold is also invisible in normal use, because interactive callers ask for
fractions of a second and only a test or a long fast-forward crosses it.

## How to apply

- Size the guard from the request, not from a constant:
  `const maxSteps = Math.ceil(seconds / MAX_STEP) + 2;`
- Validate the argument instead of absorbing it. `Number.isFinite(seconds)` and
  `seconds > 0` remove the only way the loop can fail to terminate, which is
  what the constant was really guarding against.
- Assert the whole interval was covered, not just that the call returned:
  advance by a day and check the elapsed time is a day.
- The same shape appears in retry counts, pagination page caps and chunked
  readers: any cap expressed in iterations is a cap on the input.
