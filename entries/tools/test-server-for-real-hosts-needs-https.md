---
title: A local server standing in for real domains in Chrome tests must also speak HTTPS
tags: [testing, browser, https]
added: 2026-09-23
sources:
  - https://hstspreload.org/
---

## Fact

`--host-resolver-rules` can point every hostname at one local server, which is
enough for invented hosts (`news.example`, `*.test`). Real domains are different:
Chrome rewrites requests to HSTS-preloaded domains to `https://`, and HTTPS
upgrades do the same for top-level navigations to public domains on the default
port. The TLS handshake reaches a plain HTTP server and the load fails
(`ERR_SSL_PROTOCOL_ERROR`, or an HTTPS-First error page that automation reports
as `ERR_BLOCKED_BY_CLIENT`). Disabling the `HttpsUpgrades` feature did not stop
it in current Chrome.

## Why it matters

A test asserting that something was blocked ("the server never saw the request")
passes vacuously when the request died on the upgrade instead, so the suite stays
green while checking nothing.

## How to apply

- Serve both protocols on one port: `net.createServer`, peek the first byte
  (`0x16` opens a TLS handshake), then `emit('connection', socket)` on an
  `https` or an `http` server.
- Create a throwaway certificate at test start (`openssl req -x509 -newkey
  rsa:2048 -nodes -subj /CN=test ...`) and launch Chrome with
  `--ignore-certificate-errors`; use `https://` fixture URLs throughout.
- Map the port too, `MAP * 127.0.0.1:<port>`, so URLs carry no port and
  patterns like `||host/path` match as they would in production.
- Pair every "was not requested" assertion with a run where it must arrive.
