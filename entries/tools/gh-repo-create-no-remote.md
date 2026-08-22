---
title: gh repo create does not add a git remote unless you pass --source
tags: [git, github, cli]
added: 2026-08-22
---

## Fact

`gh repo create <name>` creates the repository on GitHub and prints its URL, but
when run without `--source` it does not touch the local repository at all. There
is no `origin` afterwards, and the next `git push` fails.

The failure message is about access rights and repository existence:

```
Please make sure you have the correct access rights
and the repository exists.
```

which points at authentication or a typo — neither of which is the actual cause.
The repository does exist, and the token is fine; git simply resolved `origin` as
a literal remote name that was never defined.

## Why it matters

`gh repo create` succeeding, and printing a working URL, reads as "the repo is
wired up". The gap between the remote existing and the local clone knowing about
it is invisible until the push, and the error then sends you to check `gh auth
status` and repository visibility, which are both healthy.

## How to apply

- Pass `--source` when a local repository already exists:
  `gh repo create <name> --public --source=. --remote=origin`
- Otherwise add the remote yourself before the first push:
  `git remote add origin https://github.com/<owner>/<name>.git`
- When a push fails with "make sure you have the correct access rights", run
  `git remote -v` before investigating credentials. Empty output is this bug.
