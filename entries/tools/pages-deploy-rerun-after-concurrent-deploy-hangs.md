---
title: Never re-run a Pages deploy rejected for an in-progress deployment; the stuck re-run blocks every later deploy
tags: [github-pages, github-actions, ci]
added: 2026-11-01
updated: 2026-11-01
---

## Fact

Two pushes a few seconds apart can make the built-in "pages build and
deployment" workflow fail with `Deployment request failed ... due to in
progress deployment`. Re-running that failed run can leave it `queued` with
no jobs, and it never starts. A new build from the Pages API runs normally.

## Why it matters

The stuck re-run keeps holding the Pages deploy lock. Every later deploy
fails with the same "in progress deployment" error naming that commit, even
though the Pages API reports its deployment as succeeded. The re-run cannot
be cancelled, force-cancelled (409, "has not yet queued"), deleted (403) or
re-run again ("already running"). Turning Pages off and on does not clear it
either, and leaves the site at 404 until a deploy gets through.

## How to apply

Do not press re-run on that failure. Wait for the earlier deploy to finish,
then request a fresh build of the branch head:

```bash
gh api -X POST repos/OWNER/REPO/pages/builds
```

Space out pushes to a Pages branch by a minute or two to avoid the clash.

If a re-run is already stuck, delete the `github-pages` environment; the
next build recreates it and deploys. Note its branch policy first and put it
back afterwards, because the recreated environment has none:

```bash
gh api -X DELETE repos/OWNER/REPO/environments/github-pages
gh api -X POST repos/OWNER/REPO/pages/builds
gh api -X PUT repos/OWNER/REPO/environments/github-pages \
  -F 'deployment_branch_policy[protected_branches]=false' \
  -F 'deployment_branch_policy[custom_branch_policies]=true'
gh api -X POST repos/OWNER/REPO/environments/github-pages/deployment-branch-policies \
  -f name=main -f type=branch
```
