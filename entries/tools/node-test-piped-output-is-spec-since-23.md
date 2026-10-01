---
title: node --test prints spec, not TAP, into a pipe since Node 23, so filters for TAP lines match nothing
tags: [node, testing, ci]
added: 2026-10-02
sources:
  - https://nodejs.org/api/test.html#test-reporters
  - https://nodejs.org/docs/latest-v22.x/api/test.html#test-reporters
---

## Fact

Up to Node 22, `node --test` used the `tap` reporter whenever stdout was not a
terminal, so piped or redirected output had `ok` / `not ok` lines and a
`# pass N` / `# fail N` summary. Since v23.0.0 the default is `spec` there
too: `✔` / `✖` per test and a summary of `ℹ pass N`, `ℹ fail N`. Nothing
warns about the change.

## Why it matters

A script or CI step that greps the piped output for TAP lines (`^not ok`,
`^# fail`) matches nothing at all on every release since 23, LTS lines
included, and an empty match is easily read as zero failures. The same
`npm test | grep ...` answers differently on two machines whose only
difference is the Node major.

## How to apply

- Decide pass or fail by the exit code, which is non-zero on any failure
  with every reporter; never by the absence of a failure line.
- When a tool must parse the results, name the reporter instead of relying
  on the default: `--test-reporter=tap`, or `--test-reporter=junit
  --test-reporter-destination=results.xml` for CI dashboards.
- To skim a long run by eye on 23+, filter for `^ℹ ` (the summary) and `✖`
  (failures).
