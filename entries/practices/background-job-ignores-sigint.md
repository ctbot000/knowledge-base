---
title: A background job of a non-interactive shell starts with SIGINT ignored, so kill -INT tests nothing
tags: [shell, signals, testing]
added: 2026-09-24
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html#tag_19_11
  - https://docs.python.org/3/library/signal.html
---

## Fact

With job control off — `sh -c`, scripts, CI steps, agent shells — POSIX shells
start an asynchronous command (`cmd &`) with SIGINT and SIGQUIT set to
ignored. A program that installs its handler only when SIGINT is not already
ignored never hears `kill -INT`. Python is one: it maps SIGINT to
`KeyboardInterrupt` only "if the parent process has not changed it", so the
child reports `signal.getsignal(signal.SIGINT) == 1` (SIG_IGN) and keeps
running. Checked in both bash and zsh.

## Why it matters

A test that proves a server stops on Ctrl+C by sending SIGINT to a backgrounded
copy sees it keep running and blames the shutdown code, while the same program
stops instantly in a real terminal. A harness that relies on SIGINT to end a
child leaks it instead.

## How to apply

- bash: `set -m` before launching restores the default (the child then exits
  on SIGINT at once). zsh refuses `set -m` in a non-interactive shell.
- From Python: `subprocess.Popen(cmd, preexec_fn=lambda:
  signal.signal(signal.SIGINT, signal.SIG_DFL))`.
- Stop background children with SIGTERM; test Ctrl+C handling separately.
- Check what the child inherited:
  `python3 -c 'import signal; print(signal.getsignal(signal.SIGINT))'` —
  `1` means ignored.
