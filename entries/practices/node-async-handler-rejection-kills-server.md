---
title: An async request handler that throws kills Node's whole HTTP server by default
tags: [node, http, error-handling]
added: 2026-09-28
sources:
  - https://nodejs.org/api/cli.html#--unhandled-rejectionsmode
  - https://nodejs.org/api/events.html#capture-rejections-of-promises
---

## Fact

`http.createServer(async (req, res) => …)` ignores the promise the handler
returns. Anything the handler throws and does not catch becomes an unhandled
rejection, and under Node's default `--unhandled-rejections=throw` (since v15)
that ends the process: one bad request drops every connection. Under `warn`
the process survives, but that request is never answered and the client waits
out its own timeout.

## Why it matters

Handlers usually wrap routing and business logic in try/catch and then write
the response after it. The write can throw too: `res.setHeader(name, undefined)`
raises `ERR_HTTP_INVALID_HEADER_VALUE`, and `JSON.stringify` throws on a BigInt
or a cycle. So the crash comes from the one line nobody guarded. Under
`node:test` the same bug shows up as a hung request rather than a crash.

## How to apply

- Keep the whole handler, the response write included, inside try/catch, with
  a last-resort 500: remove the headers set so far, or destroy the socket if
  they were already sent.
- Catch where the handler is registered:
  `createServer((req, res) => handle(req, res).catch(log))`.
- Or opt in to Node's own fallback: set `events.captureRejections = true`
  before creating the server. `http.Server` then answers a rejected handler
  with a bare 500 instead of crashing.
- Test the fallback: make the response-building code throw on purpose and
  assert the client gets a 500 promptly.
