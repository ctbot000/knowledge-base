---
title: Markdown strips the backslash from `\{`, `\\` and `\,` inside math, GitHub.com included
tags: [markdown, mathjax, github]
added: 2026-09-25
sources:
  - https://spec.commonmark.org/0.31.2/#backslash-escapes
  - https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions
---

## Fact

GitHub.com's renderer and CommonMark under Jekyll both apply backslash escapes
inside `$…$` and `$$…$$` as they would anywhere else. A backslash before ASCII
punctuation is dropped, so TeX's punctuation commands reach MathJax without
theirs: `\{` becomes `{`, `\\` becomes `\`, and `\,` becomes `,`. Control words
(a backslash followed by letters, such as `\lbrace`) are not escapes and pass
through untouched.

## Why it matters

Nothing errors, because what is left is still valid TeX that means something
else. `\{0,1,2\}` renders as a bare `0,1,2`, since `{…}` is only a group. `\\`
stops breaking rows, so `cases` and `aligned` collapse onto one line. `\,` prints
a literal comma. The source looks right in an editor, so the fault shows only on
the rendered page.

## How to apply

Write the control-word form, which every renderer leaves alone:

- `\{` `\}` → `\lbrace` `\rbrace`
- `\\` between rows → `\cr`
- `\,` `\;` `\!` → `\thinspace` `\medspace` `\negthinspace`
- `\|` → `\Vert`

Doubling the backslash (`\\{`) survives one Markdown pass. A renderer that keeps
math verbatim, however, reads it as a row break. GitHub's `` $`…`$ `` delimiters
protect the content too, but only on GitHub.com. Elsewhere they make a code span,
which MathJax skips.
