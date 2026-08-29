---
title: Enabling GitHub Pages from the CLI is an API POST, and its success does not mean the site is live
tags: [github, github-pages, cli]
added: 2026-08-29
sources:
  - https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site
  - https://cli.github.com/manual/gh_api
---

## Fact

`gh` has no `pages` command. Turning Pages on for a repository is a `POST` to
`repos/{owner}/{repo}/pages`, and the `source` object it requires is written with
bracketed `-f` keys, not as JSON:

```bash
gh api -X POST repos/OWNER/REPO/pages -f "source[branch]=main" -f "source[path]=/"
```

The response comes back immediately with `html_url` already filled in and
`"status": null` — no build has run yet. The status then moves to `building` and
only later to `built`, tens of seconds afterwards.

## Why it matters

The populated `html_url` in the response reads as "the site is up", so a script
that creates Pages and then fetches the URL — or an agent that reports the link
to a user — is racing a build that has not started. Nothing is published at that
path yet, so the fetch fails in a way that looks like a broken deployment rather
than an unfinished one.

The `-f` shape is the other half: `-f` takes flat `key=value` pairs, so an
endpoint wanting a nested object needs the bracket form. `-f source=main` cannot
express it, and the error is about the field rather than about Pages.

## How to apply

- Poll the resource until the build lands, before announcing the URL:

  ```bash
  until [ "$(gh api repos/OWNER/REPO/pages --jq .status)" = built ]; do sleep 10; done
  ```

- Treat `errored` as a stop condition too; `gh api repos/OWNER/REPO/pages/builds/latest
  --jq .error.message` says why.
- Use bracketed keys for any nested object an endpoint wants, not only this one.
