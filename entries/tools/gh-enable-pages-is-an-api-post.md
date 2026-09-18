---
title: Enabling GitHub Pages from the CLI is an API POST, and its success does not mean the site is live
tags: [github, github-pages, cli]
added: 2026-08-29
updated: 2026-09-18
sources:
  - https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site
  - https://cli.github.com/manual/gh_api
---

## Fact

`gh` has no `pages` command. Turning Pages on for a repository is a `POST` to
`repos/{owner}/{repo}/pages`, and the `source` object a branch-built site needs
is written with bracketed `-f` keys, not as JSON:

```bash
gh api -X POST repos/OWNER/REPO/pages -f "source[branch]=main" -f "source[path]=/"
gh api -X POST repos/OWNER/REPO/pages -f build_type=workflow   # built by Actions
```

Either way the response comes back immediately with `html_url` already filled in
and `"status": null` — no build has run yet. What that status does next depends
on the builder. A branch-built site moves to `building` and then to `built`. A
workflow-built one never reports a status at all: `.status` stays `null` for the
life of the site and `pages/builds/latest` answers 404, because both describe
the legacy builder only.

## Why it matters

The populated `html_url` reads as "the site is up", so a script that creates
Pages and then fetches the URL — or an agent that reports the link to a user —
is racing a build that has not started.

The obvious guard against that, polling until `.status` is `built`, then hangs
forever on a workflow-built site. The field it waits on is not merely unset yet;
it is never written.

## How to apply

- Branch-built — poll the resource, treating `errored` as a stop condition:

  ```bash
  until [ "$(gh api repos/OWNER/REPO/pages --jq .status)" = built ]; do sleep 10; done
  ```

- Workflow-built — wait on the run, then on the deployment
  (`gh api repos/OWNER/REPO/deployments --jq '.[0].environment'` is
  `github-pages`), or simply fetch the URL and require a 200.
- Use bracketed keys for any nested object an endpoint wants, not only this one.
