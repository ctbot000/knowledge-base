---
title: node --test waits forever for a hung test, and --test-timeout alone does not end the run
tags: [node, testing, ci]
added: 2026-09-28
sources:
  - https://nodejs.org/api/cli.html#--test-timeout
  - https://nodejs.org/api/cli.html#--test-force-exit
---

## Fact

`--test-timeout` defaults to `Infinity`, so a test awaiting a response that
never comes stalls the whole run. Setting a timeout makes that test give up,
but its file's process keeps running while a listening server or an open
socket holds the event loop, so the run still never finishes. Only a teardown
that closes those handles, or `--test-force-exit`, lets it exit. The summary
counts a timed-out test as `cancelled`, not `fail`; the exit code is 1 either
way.

## Why it matters

The hang appears exactly when a bug stops a server from answering. A failure
in the code under test becomes a CI job that sits silent until the job's own
limit (six hours by default on GitHub Actions). Fault injection and mutation
testing hit this constantly.

## How to apply

- `"test": "node --test --test-timeout=10000 --test-force-exit"`. Both are
  flags, not positionals, so this keeps the portable bare-`node --test`
  discovery. They need Node 20.14+ (force-exit) and 20.11+ (timeout).
- Bound teardown too: `server.close()` waits for the hung connection. Call
  `server.closeAllConnections()` in `after`, or force it after a short grace.
- A hang in every test of a file costs the timeout once per test. Keep the
  timeout close to the slowest real test, not generous.
- When a CI check parses the summary, treat `cancelled > 0` as a failure.
