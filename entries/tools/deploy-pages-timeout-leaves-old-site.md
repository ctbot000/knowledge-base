---
title: A deploy-pages job that times out while syncing files leaves the old site live
tags: [github-pages, github-actions, ci]
added: 2026-11-08
---

## Fact

`actions/deploy-pages` can sit in `Current status: syncing_files` until the
job's `timeout-minutes` cancels it. The action then cancels the Pages
deployment, and the site keeps serving the previous commit. Re-running the
failed job reuses the run's artifact and normally deploys within a minute
or two.

## Why it matters

The push succeeded and nothing else looks wrong, so it is easy to report a
change as live while visitors still get the old pages. Pages also serves
files with `Cache-Control: max-age=600`, so a browser can keep stale JS and
CSS for up to ten minutes even after a good deploy.

## How to apply

After a push, check that the deploy run succeeded, not just the push:

```bash
gh run list --repo OWNER/REPO --workflow Pages --limit 1 --json headSha,conclusion
```

If the deploy job was cancelled after waiting on `syncing_files`, re-run it:

```bash
gh run rerun RUN_ID --failed --repo OWNER/REPO
```

That is a different failure from a deploy rejected for an in-progress
deployment, where a re-run can get stuck (see
[pages-deploy-rerun-after-concurrent-deploy-hangs](pages-deploy-rerun-after-concurrent-deploy-hangs.md)).
To confirm what is live, fetch a changed file from the site itself and check
its content, and reload any page opened before the deploy.
