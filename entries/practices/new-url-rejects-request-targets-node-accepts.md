---
title: new URL(req.url, base) throws on request paths Node's HTTP server accepts
tags: [node, http, url, error-handling]
added: 2026-10-05
sources:
  - https://nodejs.org/api/url.html#urlparseinput-base
  - https://url.spec.whatwg.org/#concept-basic-url-parser
---

## Fact

A request path starting with `//` is parsed by `new URL(path, base)` as an
authority, so `new URL('//[x', 'http://localhost')` throws `TypeError: Invalid
URL`. Node's HTTP server accepts that path and hands it over as `req.url`, and
ordinary clients send it: `fetch('http://host//[x')` and `http.request({ path:
'//[' })` both do.

## Why it matters

Parsing `req.url` this way is the usual first line of a handler. In a
synchronous listener such as `server.on('upgrade', …)` the throw is an uncaught
exception and ends the process, taking every open connection with it, so any
client can stop the server with one request. Tests that only request normal
paths never meet it.

## How to apply

- Parse with `URL.parse(req.url, base)` (Node 22.1+ and 20.18+), which returns
  `null` instead of throwing, and answer 400 or 404 for `null`. Elsewhere, wrap
  `new URL` in try/catch.
- Or take the path as a string (`req.url.split('?')[0]`) when only the path
  matters.
- Add a test that requests `//[` on every route that parses `req.url`,
  WebSocket upgrades included, and asserts an answer instead of a crash.
