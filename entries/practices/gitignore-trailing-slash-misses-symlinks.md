---
title: A gitignore pattern with a trailing slash does not match a symlink to a directory
tags: [git, gitignore, symlink]
added: 2026-10-05
sources:
  - https://git-scm.com/docs/gitignore
---

## Fact

A `.gitignore` pattern ending in `/` matches only directories, and git treats a
symbolic link as a file even when it points at a directory. `node_modules/`
ignores a real `node_modules` folder but not a `node_modules` symlink, which
shows up as untracked (`?? node_modules`) and is staged by `git add -A` or
`git add .`.

## Why it matters

Linking a dependency or build folder into a second checkout (a git worktree, a
copy for a quick experiment) is a common way to avoid reinstalling. The link
then gets committed: a pointer to a path on one machine, which is broken
everywhere else and can shadow the real install on the next checkout.

## How to apply

- Stage explicit paths in a checkout that holds such a link, and read
  `git status --short` before committing.
- To ignore both forms, drop the slash (`node_modules`), or add a second
  pattern for the link, preferably in `.git/info/exclude` when the link is
  local to one checkout.
- `git check-ignore -v node_modules` exits 1 and prints nothing when the path
  is not ignored.
