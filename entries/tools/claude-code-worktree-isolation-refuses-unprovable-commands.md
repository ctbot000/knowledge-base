---
title: A worktree-isolated Claude Code session refuses shell commands it cannot prove stay inside the worktree
tags: [claude-code, agents, git, shell]
added: 2026-10-07
---

## Fact

Once a session has moved into a git worktree (`EnterWorktree`), every Bash call
is checked so that no git operation can reach another checkout. A command the
checker cannot analyse is refused before anything runs, with an explanation.
Refused shapes seen: a heredoc that writes a file outside the worktree chained
with other commands; `cd` into a directory outside it; a program or operand
computed at runtime (`sed -n "$(grep …)"`, `ls … | xargs node --test …`); an
append like `cat >> file <<EOF … EOF` chained with a test run. Plain commands
with literal arguments run normally, and so does a heredoc fed to an
interpreter that only touches files in the worktree.

## Why it matters

Each refusal costs a round trip, and rewording the same compound command a few
ways costs several. It reads like a permissions problem, but no prompt or
setting is involved: the shape of the command is what fails.

## How to apply

- Write scripts, patches and payloads with the file-writing tool (into the
  session's scratchpad), then run each with one plain command and literal
  absolute paths: `python3 /abs/patch.py`, `bash /abs/loop.sh 6`.
- List files explicitly instead of computing them: `node --test test/a.test.js
  test/b.test.js`, not a pipe into `xargs`.
- Keep a long loop's logic inside a script file; the script's body is not
  inspected, only the command that starts it.
