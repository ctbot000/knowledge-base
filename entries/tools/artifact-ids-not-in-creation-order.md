---
title: GitHub Actions artifact IDs are not assigned in creation order
tags: [github-actions, artifacts, ci]
added: 2026-10-09
sources:
  - https://github.com/actions/toolkit/pull/2540
---

## Fact

An artifact's ID (`id` in the REST API, `databaseId` in the artifact service)
does not grow with upload time, not even within one run. Four matrix jobs of one
run, uploading over 19 seconds, got IDs 10696995222, 10696442090, 10696412148
and 10696746841 in that order, and a re-run's artifact got a lower ID than the
first attempt's. Across 37 artifacts in 7 repositories, the later of two
artifacts had the lower ID in about 2% of pairs.

## Why it matters

"Highest ID is newest" silently picks an older artifact. `@actions/artifact`
6.3.1 and earlier does exactly that when several artifacts share a name, as
after a re-run that uploads again: `getArtifact` and
`listArtifacts({latest: true})`, and so `download-artifact` by name, can return
the previous attempt's artifact.

## How to apply

- Order artifacts by `created_at` and use the ID only to break ties.
- To fetch an artifact uploaded earlier in the run, pass the `artifact-id`
  output of `upload-artifact` to `download-artifact`'s `artifact-ids` input
  instead of looking it up by `name`.
