---
title: deploy-pages can miss an artifact uploaded a moment earlier in the same job
tags: [github-actions, github-pages, ci]
added: 2026-10-09
sources:
  - https://github.com/actions/deploy-pages/issues/451
  - https://github.com/actions/deploy-pages/issues/338
---

## Fact

`actions/deploy-pages` lists the run's artifacts once and fails if none is named
`github-pages`. Right after `upload-pages-artifact` finalizes, that list can
still be empty, so the single-job layout — upload, then deploy as the next step,
as in GitHub's static starter workflow — fails now and then with
`No artifacts named "github-pages" were found`, even with matching action
versions. One repository saw it once in 63 deploys.

## Why it matters

The error text points at old `upload-artifact` versions, and its advice to
re-run makes things worse: the re-run uploads a second `github-pages` artifact
to the same run and fails with `Multiple artifacts named "github-pages"`. Only a
new run recovers.

## How to apply

Upload in an earlier job and deploy in a later one. Make
`upload-pages-artifact` the last step of the build or test job, under the same
branch condition as the deploy, and let the `needs:` deploy job run only
`deploy-pages`. The job boundary puts seconds between upload and lookup, and
"Re-run failed jobs" then re-runs only the deploy, which finds the one artifact.
