---
title: A repository's Pages URL is usually absent from its `homepage` field
tags: [github, github-pages, api]
added: 2026-09-10
sources:
  - https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user
---

## Fact

`has_pages` on the repos listing is a reliable flag for "this repository serves a
GitHub Pages site", and it needs no authentication for public repositories. The
URL, however, is not there: `homepage` is a field the owner sets by hand, so it
is `null` on most repositories that publish Pages, and enumerating sites by
filtering on a non-empty `homepage` silently misses them.

The project-site URL is derivable instead — `https://<owner>.github.io/<repo>/`,
or `https://<repo>/` when the repository is named `<owner>.github.io`.

## Why it matters

The obvious query returns a partial list that looks complete, because every entry
in it is correct. There is no error and no empty result to notice — just fewer
sites than the account actually has.

`GET /repos/{owner}/{repo}/pages` does return the real URL, but it needs push
access, so it is unavailable for enumerating someone else's sites and unavailable
to a CI token scoped to a different repository.

## How to apply

```sh
gh api --paginate "users/OWNER/repos?per_page=100" \
  --jq '.[] | select(.has_pages and (.archived | not)) | .name'
```

- Build the URL from the repo name; fall back to `homepage` only when it is set
  and points off `github.com`, which is how a custom domain shows up.
- Filter out `archived` repositories — the flag stays true after archiving.
