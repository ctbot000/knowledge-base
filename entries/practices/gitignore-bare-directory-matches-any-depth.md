---
title: A gitignore pattern with no slash matches at every depth, so it can swallow a source directory
tags: [git, gitignore, java]
added: 2026-09-22
sources:
  - https://git-scm.com/docs/gitignore
---

## Fact

A `.gitignore` pattern that contains no slash other than a trailing one matches
anywhere in the tree, not just at the repository root. `target/` — copied into
almost every JVM project's ignore file for Maven's output — also ignores
`src/main/java/com/example/target/`, and `build/`, `bin/` and `out/` behave the
same way.

## Why it matters

`git add` reports nothing, `git commit` succeeds, and the push goes out with a
whole package missing. The local build keeps passing because the files are still
on disk; the first symptom is CI failing to compile, or a fresh clone missing
code that "is definitely committed".

## How to apply

- Anchor build-output patterns to the root with a leading slash: `/build/`,
  `/target/`, `/out/`, `/bin/`.
- Before the first push of a new repository, read the staged list rather than
  trusting the command: `git status --short` or
  `git diff --cached --name-only`. A commit hash proves a commit happened, not
  that it contains what you think.
- `git check-ignore -v <path>` names the pattern and the file it came from when
  something is missing.
