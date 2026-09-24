---
title: A Go handler that fails mid-body must panic(http.ErrAbortHandler), or the client gets a clean end
tags: [go, http, streaming]
added: 2026-09-24
sources:
  - https://pkg.go.dev/net/http#ErrAbortHandler
---

## Fact

Once a Go `net/http` handler has started a response without a
`Content-Length` (a chunked body: a streamed archive, export or proxy), simply
returning after a source-side error makes the server finish the body with its
terminating chunk. The client sees a complete, successful response. Only
`panic(http.ErrAbortHandler)` makes the server drop the connection without the
final chunk, so the client reports an error; `net/http` does not log that
particular panic.

## Why it matters

The status line has already gone out as 200, so the failure has no other way
to reach the client. A browser download of a streamed ZIP whose source file
vanished halfway is saved as finished, and only fails later, when someone
tries to open an archive with no central directory. Nothing logs an error on
either side.

## How to apply

- After the first byte is written, turn any error from the source into
  `panic(http.ErrAbortHandler)` instead of `return`.
- Responses with a correct `Content-Length` do not need it: a short body is
  already detected by the client.
- Test it: make the source fail midway and assert that `http.Get` or
  `io.ReadAll(resp.Body)` returns an error. Depending on buffering, the error
  can surface at either point.
