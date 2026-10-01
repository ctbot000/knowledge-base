---
title: A plain rebase replays the commit your branch started from when upstream has only an amended copy of it
tags: [git, rebase]
added: 2026-10-02
sources:
  - https://git-scm.com/docs/git-rebase
  - https://git-scm.com/docs/git-patch-id
---

## Fact

`git rebase <upstream>` skips a commit of yours when upstream already has the
same patch (same patch-id), or when replaying it leaves nothing to commit. An
amended copy matches neither. So when the unpushed commit your branch was cut
from is amended and pushed by someone else, a plain rebase replays the old
copy on top of the new one and conflicts in the files it touched. A copy that
was only rebased, even across edits next to it, is still skipped cleanly.

## Why it matters

Parallel worktrees make this routine: a branch is cut from a local commit that
another session later rebases, amends and pushes. The conflicts land in code
you never wrote, and resolving them by hand risks reverting or duplicating
parts of the other session's final version.

## How to apply

- Check before rebasing: `git merge-base --is-ancestor <your-base> origin/main`
  fails, and `git log origin/main..HEAD` lists commits that are not yours.
- Replay only your own commits: `git rebase --onto origin/main <your-base>`,
  where `<your-base>` is the last commit on your branch that is not yours.
