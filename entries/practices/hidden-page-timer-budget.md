---
title: A hidden page's timer budget turns setTimeout into a one-second yield, but only when there is work between yields
tags: [browser, performance, async]
added: 2026-09-08
sources:
  - https://developer.chrome.com/blog/timer-throttling-in-chrome-88/
---

## Fact

Browsers give a hidden page a wake-up budget of roughly one timer per second.
A long computation chunked with `await new Promise(r => setTimeout(r, 0))`
therefore parks until the next slot at every chunk boundary: a search that takes
three seconds in a visible tab takes sixteen in a hidden one, nearly all of it
spent waiting rather than computing.

The trap is that measuring the yield alone shows nothing. Back-to-back timers
with no work between them coalesce into a single wake-up, so a microbenchmark of
`setTimeout(0)` in the same hidden page reports **0 ms** while the real workload
pays ~0.7 s per yield.

A `MessagePort` task is not a timer and is not budgeted. Swapping the yield for
`MessageChannel` removed the entire overhead, and the per-item cost went flat.

## Why it matters

The symptom is per-item cost that *rises with item count* — a small job looks
fine, a large one is inexplicably slow — which points at the algorithm, at
allocation, or at deoptimisation, none of which is the cause. Profiling the yield
to rule it out actively confirms the wrong conclusion. It bites in exactly the
environments automated checks run in, and for any user who switches tabs.

## How to apply

- Yield with a `MessageChannel` rather than a timer when chunking work that must
  keep running off-screen:

  ```js
  const ch = new MessageChannel();
  let pending = null;
  ch.port1.onmessage = () => { const r = pending; pending = null; r?.(); };
  const yieldToPage = () => new Promise((r) => { pending = r; ch.port2.postMessage(0); });
  ```

- Guard it for non-browser runtimes: Node implements `MessageChannel` too, where
  a listening port holds the event loop open and a test run never exits. Branch
  on `typeof document`, not on whether the class exists.
- To confirm the diagnosis, compare cost per item across two job sizes. A yield
  budget shows up as a fixed cost per chunk, never as a fixed cost per item.
