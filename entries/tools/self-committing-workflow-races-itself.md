---
title: A workflow that commits to its own repository races every other trigger of itself
tags: [github-actions, ci, git]
added: 2026-09-11
---

## Fact

A generate-and-commit workflow — rebuild an index, a changelog, a manifest, then
`git add`, `git commit`, `git push` — has no protection against a second copy of
itself running at the same time. Two triggers that land within a few seconds
(a `push` and a `repository_dispatch`, a dispatch and a `schedule`) both check
out the same base commit, both regenerate, and both try to push. The first wins.
The second dies on a non-fast-forward:

```
! [rejected]  main -> main (fetch first)
```

This is the normal outcome of the documented pattern "push the change, then fire
a dispatch so the index updates immediately": the push has already started a run
of its own.

## Why it matters

The failure is reported on the run that did nothing wrong, and it inverts the
obvious reading. A red X next to "Update index" says the index did not update,
when in fact its sibling run updated it seconds earlier and the artefact is
correct and deployed. Acting on the red X means re-running, re-dispatching, or
hunting a generator bug that is not there.

The reverse case is worse and quieter: where the two runs would have produced
*different* output, the loser's work is discarded with only a failed push to
show for it.

## How to apply

- Check the artefact before believing the run. `git show origin/main:<file>`
  answers "did the work land?" directly; the run's status does not.
- Serialise the workflow rather than the triggers:

  ```yaml
  concurrency:
    group: update-index
    cancel-in-progress: false
  ```

  `cancel-in-progress: false` matters — cancelling would drop the newer
  generation, which is the one you wanted.
- Make the push step tolerate a lost race on its own:
  `git pull --rebase --autostash && git push`, and exit 0 when the regenerated
  file is unchanged.
- When a generator reads live external state rather than the repository, a lost
  race is harmless by construction — say so in the workflow, so the next person
  does not add retry logic for a problem that does not exist.
