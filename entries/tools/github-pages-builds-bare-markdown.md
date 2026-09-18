---
title: GitHub Pages builds Markdown that has no front matter, and rewrites relative `.md` links
tags: [github-pages, jekyll, static-sites]
added: 2026-09-18
sources:
  - https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
  - https://github.com/benbalter/jekyll-relative-links
---

## Fact

Stock Jekyll processes only files that carry YAML front matter and copies the
rest verbatim. GitHub Pages enables a plugin set that removes that requirement:
`jekyll-optional-front-matter` turns a bare `.md` file into a page,
`jekyll-default-layout` wraps it in the theme's layout,
`jekyll-titles-from-headings` takes its title from the first heading,
`jekyll-readme-index` promotes `README.md` to the site index, and
`jekyll-relative-links` rewrites a link like `[notes](notes.md)` to `notes.html`.

A repository whose content is already Markdown therefore becomes a site by
adding one file, and no source document is touched:

```yaml
# _config.yml
theme: jekyll-theme-primer
```

## Why it matters

The obvious assumption — every page needs front matter, and a link ending in
`.md` will 404 — leads to editing each document, or to generating HTML, for a
set of files whose whole value is being readable as plain Markdown in the repo.

The reverse trap costs more: a local `jekyll serve` without the `github-pages`
gem has none of these plugins, so it 404s pages that Pages builds fine, and the
natural fix is to add exactly the front matter that was never needed.

## How to apply

- Keep in-repo links relative and extension-ful (`notes.md`); they resolve on
  GitHub.com and are rewritten for the site.
- Keep a file out of the build with `exclude:` rather than deleting or moving it.
- Verify against the deployed site or the `github-pages` gem, never a bare local
  Jekyll.
