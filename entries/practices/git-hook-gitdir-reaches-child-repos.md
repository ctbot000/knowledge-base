---
title: A git hook run from a linked worktree hands its children GIT_DIR as a full path, so a test's git init re-creates the real repository
tags: [git, hooks, worktrees, testing]
added: 2026-10-19
sources:
  - https://git-scm.com/docs/githooks
---

## Fact

git exports `GIT_DIR` (and `GIT_INDEX_FILE` and friends) to the hooks it runs,
and a hook passes them to everything it starts. Pushed from a linked worktree,
`GIT_DIR` is the full path of that worktree's own git folder
(`.git/worktrees/<name>`), so it wins over the folder a child git command runs
in. A test that makes a scratch repository with `git init` in a temporary
folder re-initialises the real one instead — with `GIT_DIR` set and no work
tree, as bare — and its `git config user.email …` lands in the shared
`.git/config`. The same hook pushed from the main checkout did no harm.

## Why it matters

`core.bare = true` in the shared config breaks every checkout of the
repository at once ("fatal: this operation must be run in a work tree"),
including other people's and other agents' worktrees, and the test identity
it wrote becomes the author of every later commit there. The hook just
reports a few failing tests.

## How to apply

- A hook that runs tests or tools strips the variables first:
  `Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('GIT_')))`,
  or `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE …` in shell.
- Test helpers that create repositories clear `GIT_DIR` in the environment
  they pass to git; `git -C <dir>` alone does not override it.
- Repair: `git config --file <repo>/.git/config core.bare false`, and unset
  any `user.*` a test wrote there.
