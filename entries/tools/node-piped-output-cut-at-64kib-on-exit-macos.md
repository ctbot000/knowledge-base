---
title: On macOS, a Node process that dies keeps only the first 64 KiB of its piped output, its own crash report included
tags: [node, macos, stdio, pipe, debugging]
added: 2026-11-28
sources:
  - https://nodejs.org/api/process.html#a-note-on-process-io
  - https://github.com/nodejs/node/issues/19218
---

## Fact

When stdout or stderr is a pipe, Node on macOS writes to it without blocking.
If the process ends through `process.exit()`, or on an uncaught exception, what
it wrote last is cut at the pipe's 64 KiB buffer and the rest is dropped: the
reader gets exactly 65536 bytes. A process that ends on its own (empty event
loop, `process.exitCode` set) delivers everything, and a file or a terminal
gets it all. Seen with Node 24 and 26.

## Why it matters

A parent reading through a pipe (a test runner, `spawnSync`, CI, an agent's
shell, `| tail`) gets a cut report. The error message of an uncaught exception
comes after the source line it was thrown from, so when that line is long (a
minified bundle) or the message is huge, the message itself is never seen and
the crash seems to have printed only noise.

## How to apply

- To read a crash report in full, send stderr to a file (`2> err.txt`), not
  through a pipe.
- Set `process.exitCode` and let the process end, rather than calling
  `process.exit()` right after printing a lot.
- A crashed child's stderr of exactly 65536 bytes is this cut, not the whole
  report.
