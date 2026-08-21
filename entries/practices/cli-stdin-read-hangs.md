---
title: A CLI that reads piped stdin hangs when its parent leaves the pipe open
tags: [cli, stdin, io, subprocess]
added: 2026-08-21
---

## Fact

"Read stdin when it is not a TTY" is the usual way a CLI supports `cmd < file`
and `... | cmd`. It deadlocks whenever the process is launched by a parent that
creates a stdin pipe and never writes to or closes it — which is the default for
most language-level spawn helpers (Node `child_process.execFile`, Python
`subprocess.run` with `stdin=PIPE`, Go `exec.Cmd` with `StdinPipe`).

Nothing is wrong with the pipe. There is simply no EOF coming, so a read-to-end
blocks forever. The check that fails is `isatty`: it distinguishes "terminal"
from "not a terminal", not "has data" from "has no data".

## Why it matters

The failure only appears once the tool is used non-interactively — from CI, a
test harness, an editor plugin, or another agent — and it presents as an
unexplained hang with no output and no error, usually blamed on the network or
the API call that never got made. Interactive use and shell pipelines both work
fine, so it survives manual testing.

## How to apply

- Distinguish the two non-TTY cases. A regular file (`< file`) always reaches
  EOF, so read it unbounded; anything else is a pipe and needs a deadline.
- Give the pipe an idle deadline that only applies before the first byte: if
  nothing has arrived within a few hundred milliseconds, treat stdin as empty and
  continue. Once data starts flowing, read to EOF normally.
- Test it by spawning the CLI from a parent that passes a pipe it never closes.
  A shell pipeline will not reproduce the bug, because the shell closes its end.
- Prefer an explicit opt-in (`-` as the filename, or `--stdin`) when the tool has
  no strong reason to guess.
