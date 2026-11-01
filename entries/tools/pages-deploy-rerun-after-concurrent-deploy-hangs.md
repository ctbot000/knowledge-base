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
re-run again ("already running"), so the site stays frozen.

## How to apply

Do not press re-run on that failure. Wait for the earlier deploy to finish,
then request a fresh build of the branch head:

```bash
gh api -X POST repos/OWNER/REPO/pages/builds
```

Space out pushes to a Pages branch by a minute or two to avoid the clash.
