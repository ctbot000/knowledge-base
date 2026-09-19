---
title: A reset that replaces a shared state object severs every reference already held to it
tags: [javascript, state, game-design]
added: 2026-09-19
---

## Fact

A long-lived subsystem usually captures the object it talks through exactly
once, at wiring time:

```js
const state = game.input;            // captured when the listener is installed
onKeyDown = () => { state.fire = true; };
```

A `reset()` that assigns a fresh object breaks that link permanently:

```js
reset() {
  this.input = { left: false, fire: false, ... };   // new identity
}
```

Everything still runs. The subsystem writes to an object nobody reads, and the
consumer reads an object nobody writes. The same shape appears wherever a
restart rebuilds config, a buffer, a store or an event bus that other code has
already captured.

## Why it matters

The symptom is silence, not an error. In a game the world animates, waves
spawn, the clock advances — and the controls do nothing, which reads as an
input-handling bug and sends you into the event listeners, which are fine.

It also hides from tests, because a test written after the fact naturally does
`game.start()` and *then* `game.input.fire = true`, picking up the new object
and passing. Only the real wiring order — capture, then restart — fails.

## How to apply

- Reset in place: `Object.assign(this.input, DEFAULTS)`, never `this.input = {}`.
- Or hand out an accessor instead of the object, so there is nothing to capture.
- Assert identity across the boundary, since it is one cheap line:
  `const ref = game.input; game.start(); assert.equal(game.input, ref)`.
- The general rule: anything reachable from outside is part of the API, and its
  *identity* is part of the contract as much as its contents.
