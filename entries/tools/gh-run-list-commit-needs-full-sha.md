---
title: gh run list --commit matches only a full commit SHA; a short one returns an empty list
tags: [github, github-actions, cli, ci]
added: 2026-10-04
---

## Fact

`gh run list --commit <sha>` filters workflow runs by their exact `head_sha`.
Given an abbreviated SHA such as `0af2a35`, it matches nothing and prints `[]`
(or no rows) with exit status 0, while the full 40-character SHA of the same
commit lists its runs.

## Why it matters

Nothing tells the short SHA apart from "no run has started yet". A script that
waits for a commit's CI by polling until `status == completed` never sees the
run and spins until its own timeout, so a green build reads as a hung one.

## How to apply

- Expand the SHA first: `sha=$(git rev-parse HEAD)` or `git rev-parse 0af2a35`.
- In a wait loop, also treat "no run found after a minute or two" as an error,
  so a wrong filter fails loudly instead of waiting forever.
