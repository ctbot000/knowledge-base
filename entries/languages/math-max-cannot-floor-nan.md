---
title: Math.max cannot floor a NaN, so a clamped loop bound can still run zero times
tags: [javascript, numerics, simulation]
added: 2026-09-08
---

## Fact

`Math.max(1, x)` returns `NaN` when `x` is `NaN`. The idiom everyone writes to
guarantee at least one iteration —

```js
const steps = Math.max(1, Math.ceil(speed * dt / limit));
for (let i = 0; i < steps; i++) advance(h);
```

— does not guarantee it. `i < NaN` is false on the first test, so the loop body
never runs and the function returns as if it had done its work.

## Why it matters

In a simulation the iteration count is usually derived from the state itself:
speed, distance travelled, remaining error. One `NaN` anywhere in that state
turns the whole step into a silent no-op.

The wait around it then never ends, because the liveness test is normally
written as "is anything still moving?" — and `NaN !== 0` is true. So the object
is reported as live for ever, is never stepped, and never stops. Nothing on screen
moves and no error is thrown. The symptom points at the loop that hangs, several
layers below the arithmetic that actually produced the `NaN`.

## How to apply

- Clamp through an explicit finite test, never through `Math.max`:

  ```js
  const raw = Math.ceil((speed * dt) / limit);
  const steps = Number.isFinite(raw) ? Math.max(1, raw) : 1;
  ```

- Better, sanitise where the state enters the step function — that is the one
  place that sees every entity — and park anything non-finite at rest.
- Treat `x !== 0` as "live or broken", not "live". A liveness or dirty check
  written that way silently classifies `NaN` as active.
- The same holds for `Math.min` as an upper clamp, and for `Math.max(0, x)` used
  to keep a value non-negative.
