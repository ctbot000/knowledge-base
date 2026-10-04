---
title: Work pushed from a worktree never reaches a service started from the main checkout until that checkout is pulled
tags: [agents, git, worktrees, deployment]
added: 2026-10-04
---

## Fact

An agent that works in its own git worktree and pushes to the remote moves
neither the main checkout's files nor its branch: `git push origin HEAD:main`
updates the remote and `origin/main`, not local `main`, and never a working
tree. A long-running process the user started from the main checkout (a dev
server, a self-hosted backend) keeps that checkout's old code, and so does a
restart of it.

## Why it matters

"Restart the server" is then the wrong instruction: the user restarts, the
old code comes back up, and the new feature looks broken. When CI deploys the
new client elsewhere (static hosting), the mismatch hides further: the new
client asks for requests the old backend does not know, and the user sees an
empty view, not an error about versions.

## How to apply

- After pushing a change the user's running service needs, say "pull the
  checkout it runs from, then restart", with the folder named, not just
  "restart". Mention new dependencies too (`npm install`) if the lockfile changed.
- When a just-shipped feature "shows nothing", first check what the process
  runs: its working directory (`lsof -a -p <pid> -d cwd`), that folder's
  `HEAD` against the pushed commit, and the process start time against the push.
- Make the skew visible in the product: a server that logs request types it
  does not know ("update me: pull, then restart"), and a client that words
  that refusal as "the server needs an update", turn the next occurrence into
  a one-line diagnosis.
