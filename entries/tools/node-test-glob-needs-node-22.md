---
title: node --test expands glob patterns only from Node 22, and before that reports the pattern as a missing path
tags: [node, testing, ci]
added: 2026-09-12
sources:
  - https://nodejs.org/api/cli.html#--test
---

## Fact

`node --test 'tests/*.test.mjs'` does not mean the same thing on every Node
version. From Node 22 the runner expands the pattern itself. On Node 20 it
treats the argument as a literal path and stops:

```
Could not find '/…/tests/*.test.mjs'
```

Quoting the pattern in an npm script is what exposes the difference: unquoted,
the shell expands it before Node ever sees it, so the same script works — until
it runs somewhere the shell does not glob, or a directory has no match.

## Why it matters

It splits along the developer's local Node version and CI's. A script written
and passing on a current local Node fails on the older Node pinned in a
workflow, with an error that names a path that "should" exist and points at
the project layout rather than at the runtime. The suite reports zero tests
run as a hard failure, which at least is loud — but a CI matrix that only
tests one version will not tell you which side is wrong.

## How to apply

- Name the test files explicitly in the script when portability matters:
  `node --test tests/a.test.mjs tests/b.test.mjs`. It works on every version.
- Otherwise require the version that supports it, in `engines` and in CI.
- Run the suite on more than one Node version. A version-dependent invocation
  cannot pass unnoticed under a matrix, and the matrix is what catches the
  whole class, not just this member of it.
