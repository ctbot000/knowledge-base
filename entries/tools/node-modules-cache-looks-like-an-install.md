---
title: A tool that caches under node_modules/.cache makes a checkout without an install look installed
tags: [node, npm, git-worktree, caching]
added: 2026-11-26
sources:
  - https://nodejs.org/api/modules.html#loading-from-node_modules-folders
---

## Fact

Node looks for a package in every parent folder's `node_modules`, so a git
worktree kept inside the main checkout runs without an install of its own. A
tool that keeps its cache in `node_modules/.cache` creates that folder in the
worktree all the same. Package lookup still works there (the folder has no such
package, so Node goes on up), but `existsSync('node_modules')` is now true with
nothing installed.

## Why it matters

A script that uses the folder's existence to pick where packages come from, and
links or copies it into a temporary checkout outside the tree, gets
`ERR_MODULE_NOT_FOUND` for every package. Tests run in the worktree itself still
pass, so it looks as if the script or the commit were broken.

## How to apply

Test for an install, not for the folder: npm 7 and later write a hidden lockfile.

```js
const installed = (dir) => existsSync(join(dir, 'node_modules/.package-lock.json'));
```

Write caches only where `node_modules` already exists, or in a folder of their
own. To recover, delete the worktree's `node_modules` once you have seen that it
holds only `.cache`.
