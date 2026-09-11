---
title: Serializing a self-committing workflow does not stop its push being rejected
tags: [github-actions, ci, git]
added: 2026-09-11
updated: 2026-09-11
---

## Fact

A workflow that regenerates a file and commits it back to its own repository
races every other trigger of itself, and a `concurrency` group does **not** fix
that race. GitHub pins `github.sha` when a run is *created*, and `actions/checkout`
checks out that SHA. Two triggers arriving together — a push and the dispatch
that follows it, a dispatch and the schedule — therefore resolve to the *same*
base commit. `cancel-in-progress: false` makes the second run wait its turn, but
it never re-resolves its base: it starts, checks out the commit its sibling has
already pushed past, and its own commit is a non-fast-forward:

```
! [rejected]  main -> main (fetch first)
```

Serializing decides who loses the push. It cannot stop someone losing it.

## Why it matters

The concurrency group is the obvious fix, it looks like it worked — the runs
genuinely stop overlapping — and the red X keeps appearing anyway, so the next
person re-adds a group that is already there. Meanwhile the failure is reported
on the run that did nothing wrong: its sibling generated the same bytes seconds
earlier, so the artefact is correct and deployed while the log says otherwise.

## How to apply

- Keep the group — it stops two generators running at once — but put the
  recovery in the push step: on rejection, `git fetch origin <branch>`,
  `git reset --hard FETCH_HEAD`, regenerate, retry, bounded to a few attempts.
- Discard-and-regenerate beats `git pull --rebase` here: both sides rewrote the
  same generated file, so a rebase conflicts, while rebuilding on the new base
  cannot — provided the output is a pure function of state *outside* the
  repository. Verify that before relying on it.
- The regenerated file usually matches what the winner pushed, so an "unchanged
  → exit 0" early-out at the top of the retry loop ends the run green.
- To check whether queueing is working at all, read the *job's* `started_at`,
  not the run's: `run_started_at` is set at creation even for a queued run.
