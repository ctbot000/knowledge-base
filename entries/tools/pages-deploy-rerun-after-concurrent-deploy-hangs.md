---
title: A Pages deploy rejected for an in-progress deployment cannot be fixed by re-running it; request a new build
tags: [github-pages, github-actions, ci]
added: 2026-11-01
---

## Fact

Two pushes a few seconds apart can make the built-in "pages build and
deployment" workflow fail with `Deployment request failed ... due to in
progress deployment`. Re-running that failed run can leave it `queued` with
no jobs, and it never starts. A new build from the Pages API runs normally.

## Why it matters

The site stays on the older commit while every check looks fine, and the
re-run sits in the queue forever. Builds API status stays `building`.

## How to apply

Skip the re-run. Request a fresh build of the branch head:

```bash
gh api -X POST repos/OWNER/REPO/pages/builds
```

Then watch the new run (`gh run list`) and check the live page. A leftover
queued re-run with no jobs cannot be cancelled and does no harm.
