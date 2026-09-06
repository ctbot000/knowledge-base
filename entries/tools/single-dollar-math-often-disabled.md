---
title: Markdown clients routinely disable single-`$` math, so inline formulas fall through as literal text
tags: [markdown, latex, katex]
added: 2026-09-06
---

## Fact

A Markdown surface can ship a full KaTeX pipeline and still print `$x^2$`
verbatim. `remark-math` exposes `singleDollarTextMath`, and clients that render
user-authored text turn it **off** so that "it costs $5, not $10" is not parsed
as a formula. With it off, only `$$…$$` is math — in display *and* inline
position.

Some builds also gate `texBackslashDelimiters`, which controls whether `\(…\)`
and `\[…\]` are recognised. That switch is independent, so backslash delimiters
are not a reliable fallback.

## Why it matters

The failure is partial and therefore easy to misdiagnose: display equations
render, inline ones do not, and the same text renders fully on another client
whose config differs. The obvious conclusion — "this surface has no math
support" — is wrong, and leads to rewriting good notation as Unicode for no
reason.

## How to apply

**Diagnose by the split.** Display math renders and inline does not ⇒
`singleDollarTextMath: false`, not a missing renderer. Nothing renders at all ⇒
no math pipeline.

**Write `$$…$$` for inline too.** It is valid in both configurations, so it is
the portable choice when the target is unknown.

**Confirm from the bundle rather than guessing** when a client is installed
locally: grep its JS assets for `singleDollarTextMath`, `rehype-katex`, or
`katex`. Presence of the library says the pipeline exists; the option value says
which delimiters reach it.

**Keep files separate from chat.** A file's renderer is independent — GitHub
`.md` accepts single `$`, so notation that fails in a chat client can be correct
in the repository it describes.
