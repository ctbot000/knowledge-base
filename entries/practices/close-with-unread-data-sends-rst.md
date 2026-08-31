---
title: Closing a socket with unread data sends RST, which can destroy what you just wrote
tags: [tcp, sockets, networking]
added: 2026-08-31
---

## Fact

When a TCP socket is closed while unread bytes are still sitting in its receive
queue, the kernel sends RST rather than FIN. An arriving RST entitles the peer's
stack to discard data it has received but not yet handed to the application, and
turns the peer's next read into `ECONNRESET` instead of the bytes it was about
to return.

This is exactly the shape of a rejection: write "you cannot join, because X",
then close. If the client sent anything the server chose not to read — a
pipelined message, the rest of an oversized line, a second request — the reason
can be destroyed by the RST that the close itself triggers.

## Why it matters

It is timing-dependent, so it survives local testing: the message usually
arrives, and only sometimes does the peer report a bare connection reset with no
explanation. The reset then gets blamed on the network or on a crash, while the
server's logs show it wrote a perfectly good error message.

## How to apply

- Half-close before closing: `shutdown(SHUT_WR)`, `writer.write_eof()` in
  asyncio, `CloseWrite()` on a Go `TCPConn`. The peer gets FIN and reads
  everything already in flight.
- Then read until EOF, bounded by a short timeout, and only then close. That
  drains the receive queue, so nothing is left to trigger the RST.
- Never stop reading a connection you still intend to write an error to.
- Reproduce it by making the client send more than the server reads before the
  server closes; a client that sends one line and waits will not show it.
