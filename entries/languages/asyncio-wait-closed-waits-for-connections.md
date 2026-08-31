---
title: asyncio's Server.wait_closed() waits for live connections, not just the listener
tags: [python, asyncio, networking, shutdown]
added: 2026-08-31
sources:
  - https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.Server.wait_closed
---

## Fact

Since Python 3.12, `Server.wait_closed()` returns only once the listening
sockets are closed **and every connection handler has finished**. Before 3.12 it
returned as soon as the server itself was closed, however many clients were
still connected. `async with server:` exits through the same call.

So a shutdown written as "close the server, await `wait_closed()`, then tell the
clients to leave" never reaches step three. The handlers are parked in a read
that ends only when their peer goes away, and the peers are waiting to be told.

## Why it matters

Shutdown is the least exercised path in a server, and this failure has no
traceback: the loop sits in `select()` forever. The same code was correct on
3.11, so it reads as a hang introduced by the runtime rather than by the order
of two lines.

## How to apply

- Order shutdown: `server.close()` (stop accepting) → tell connected clients to
  go → await the handler tasks with a timeout, cancelling stragglers →
  `wait_closed()` last, when it is guaranteed to return promptly.
- Keep your own set of handler tasks. The `Server` object does not expose them,
  and shutdown needs to wait on them deliberately rather than blindly.
- Do not use `async with server:` when handlers can outlive the listener; its
  `__aexit__` awaits `wait_closed()` with no timeout.
- Bound the final `wait_closed()` in `wait_for()` anyway — a client that has
  stopped reading can otherwise keep a handler alive.
