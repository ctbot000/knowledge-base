---
title: Node 21+ has a getter-only navigator global, so assigning a test stub throws in ES modules and is ignored in scripts
tags: [node, testing, javascript]
added: 2026-10-01
sources:
  - https://nodejs.org/api/globals.html#navigator
---

## Fact

Since Node 21, `globalThis.navigator` exists (`userAgent` is `"Node.js/<major>"`)
and is an accessor with a getter and no setter. `globalThis.navigator = stub`
throws `TypeError: Cannot set property navigator of #<Object> which has only a
getter` in an ES module, and in a sloppy CommonJS script it silently does
nothing, leaving the real object in place.

## Why it matters

Unit tests that run browser code in Node by stubbing `navigator` (iOS
`standalone`, `userAgent`, `clipboard`, `mediaDevices`) break on upgrade: an ESM
suite dies at the assignment, and a CommonJS one keeps running against Node's
own navigator, so properties the stub set read `undefined` and the code under
test silently takes the "not a browser" path. Feature checks like
`typeof navigator !== 'undefined'` also start reporting Node as a browser.

## How to apply

Install and restore the stub through property descriptors:

```js
const real = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
Object.defineProperty(globalThis, 'navigator', { value: { standalone: false }, configurable: true });
// ...test...
Object.defineProperty(globalThis, 'navigator', real);
```

Or run the suite with `--no-experimental-global-navigator`. Detect a browser by
`typeof document`, not by `navigator`.
