---
title: A file named INDEX.md stops jekyll-readme-index from publishing the README
tags: [github-pages, jekyll, static-sites]
added: 2026-09-06
sources:
  - https://github.com/benbalter/jekyll-readme-index
---

## Fact

`jekyll-readme-index`, one of the plugins GitHub Pages enables by default,
promotes `README.md` to a directory's index only when that directory has no
index already. The test matches built URLs against `index\.(html?|xhtml|xml)$`
**case-insensitively**, so a repository whose table of contents is `INDEX.md` —
built to `/INDEX.html` — counts as already having one.

The README is then left as a static file, served as raw Markdown, and the site
root returns 404. `readme_index: {with_frontmatter: true}` does not help: the
same guard runs before it.

## Why it matters

Nothing reports the problem. The build succeeds, every other page works, and
only `/` is missing — which looks like a propagation delay rather than a
configuration result, so the obvious response is to wait rather than to look.

## How to apply

Do not rely on the plugin. Give one page the root explicitly:

```yaml
---
layout: default
permalink: /
---
```

Name that file anything but `index.md` when the repository already has an
`INDEX.md`: on a case-insensitive filesystem (macOS by default) the two are the
same file, so creating one overwrites the other. `home.md` with the permalink
above is safe. Exclude `README.md` from the build if it should not also be
served as raw Markdown.
