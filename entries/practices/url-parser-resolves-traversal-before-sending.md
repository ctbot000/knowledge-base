---
title: fetch() and browsers resolve `..` and `%2e%2e` path segments before sending, so they cannot test path traversal
tags: [testing, security, http, url]
added: 2026-09-30
sources:
  - https://url.spec.whatwg.org/#single-dot-path-segment
  - https://url.spec.whatwg.org/#double-dot-path-segment
---

## Fact

WHATWG URL parsing, which `fetch()` uses in browsers and in Node, removes dot
segments while building the URL. A segment counts as `..` when it is `..` or
any percent-encoded spelling of it (`%2e%2e`, `.%2E`, ...), so
`fetch('/js/%2e%2e/%2e%2e/secret')` requests `/secret`. A segment that merely
contains an encoded slash, such as `/%2e%2e%2fsecret`, is left alone and does
reach the server.

## Why it matters

A traversal test built on `fetch()` sends an innocent path. Asserted as
"must not be 200" it passes vacuously, since the server was never asked for
anything outside its root; asserted as "must be 403" it fails with a 404 and
points at the server's guard, which is fine. Either way the guard the test
names is not what it exercises.

## How to apply

- Send the raw path: `http.request({ host, port, path: '/js/../../package.json' })`
  in Node, `curl --path-as-is`, or a hand-written request over a socket.
- Cover both shapes: literal `../` segments and encoded ones that survive
  parsing (`%2e%2e%2f`, `..%2f`), since the server decodes those itself.
- Keep the server-side check on the resolved path (resolve, then require it to
  stay under the root) rather than on the raw string.
