---
title: kramdown turns any line containing a pipe into a table; GitHub's renderer does not
tags: [github-pages, jekyll, markdown]
added: 2026-09-06
sources:
  - https://kramdown.gettalong.org/syntax.html#tables
  - https://github.github.com/gfm/#tables-extension-
---

## Fact

Jekyll's default Markdown processor is kramdown, whose table syntax needs **no
`|---|` delimiter row**: one line containing `|` characters is a complete
one-row table. GFM — what GitHub.com renders repository Markdown with —
requires the delimiter row, so the same line is ordinary prose there.

A sentence such as `Tangency turns into $|a|=|b|=r$, so …` therefore reads
correctly in the repository and is rebuilt as a five-cell table on the GitHub
Pages site generated from that identical file.

## Why it matters

The corruption is silent and content-dependent: the build succeeds, most pages
are fine, and only the lines that happen to contain a pipe are wrong — so it
surfaces as "this one page looks broken" long after the setup was verified.
Pipes are common in prose about absolute values, norms, `P(A|B)`, set-builder
notation, divisibility, and shell pipelines.

## How to apply

Render the site with the processor GitHub itself uses, rather than escaping
pipes by hand forever:

```yaml
markdown: CommonMarkGhPages
commonmark:
  options: [SMART, FOOTNOTES, UNSAFE]
  extensions: [strikethrough, autolink, table, tagfilter]
```

`jekyll-commonmark-ghpages` ships with the `github-pages` gem, so no plugin
declaration is needed. Note the knock-on effect on math: kramdown rewrites
display `$$…$$` to `\[…\]` while CommonMark leaves it alone, so configure
MathJax for both delimiter pairs.
