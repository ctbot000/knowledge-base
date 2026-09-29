---
title: Markdown bold that ends in punctuation cannot close right before Korean, Japanese or Chinese text
tags: [markdown, github, cjk]
added: 2026-09-29
sources:
  - https://spec.commonmark.org/0.31.2/#right-flanking-delimiter-run
  - https://github.github.com/gfm/#right-flanking-delimiter-run
---

## Fact

In CommonMark and GFM, a closing `*` or `**` that follows punctuation counts as
closing only when whitespace or more punctuation comes after it. A Hangul
particle, kana or hanzi is neither, so `**"사과"**를`, `**「東京」**に` and
`**apple.**은` render with the asterisks left in as literal text. With no
punctuation at the edge, the same run closes: `**사과**를` renders bold.

The opening side mirrors it: `**` after a letter and before punctuation cannot
open, and the stray delimiters can then pair with a later `**` and bold a span
nobody marked.

## Why it matters

Korean attaches particles directly to the word, and Japanese and Chinese use no
spaces at all, so the failing position is the normal one in CJK prose. Nothing
errors: GitHub.com shows raw `**` or bolds the wrong text, and only on the lines
where the emphasized text happens to start or end with a quote, bracket or
period.

## How to apply

- Keep punctuation outside the emphasis: `"**사과**"를`, `**사과**(apple)를`.
- When the punctuation belongs inside, use HTML: `<strong>"사과"</strong>를`.
- Use `*`, never `_`, next to CJK text: underscores do not close inside a word
  at all, so `_사과_를` fails even with no punctuation.
- Do not add a space before the particle to make it render; that changes the
  text.
- Check a doubtful line with GitHub's own renderer:
  `gh api markdown -f mode=markdown -f text='**"사과"**를'`.
