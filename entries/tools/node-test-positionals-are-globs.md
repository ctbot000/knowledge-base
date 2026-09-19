---
title: A positional argument to `node --test` is a glob pattern, never a directory to search
tags: [node, testing, ci]
added: 2026-09-12
updated: 2026-09-19
sources:
  - https://nodejs.org/api/test.html
  - https://nodejs.org/api/cli.html#--test
---

## Fact

The test runner matches positional arguments as `glob(7)` patterns. It does not
accept a directory, and it never did in the way `node --test tests/` looks like
it should. On Node 26 that argument is handed to the module loader instead, so
the process dies before a single test runs:

```
Error: Cannot find module '/…/tests'
```

`tests`, `./tests` and `tests/` all fail identically. The glob support itself
arrived in Node 22; on Node 20 a quoted pattern is treated as a literal path and
reported as `Could not find '/…/tests/*.test.mjs'`.

So each form breaks on a different runtime, and only two are safe everywhere:
explicit file names, or no argument at all — bare `node --test` runs the default
recursive search from the working directory.

## Why it matters

Both failures name a path that plainly exists, so they read as a project-layout
problem rather than a runtime one. The directory form is the worse of the two:
its error comes from the CJS loader, mentions no test and no glob, and an
unquoted glob in an npm script hides the whole class because the shell expands
it first — until it runs somewhere that does not glob, or matches nothing.

## How to apply

- Prefer bare `node --test` in the script. It works on every version, and the
  default patterns already cover `*.test.js`, `test/**` and the rest.
- Otherwise name the files: `node --test tests/a.test.mjs tests/b.test.mjs`.
- Reach for a quoted glob only with Node 22+ required in `engines` and in CI.
- Treat "zero tests ran" as a failure in CI, not as an empty suite.
