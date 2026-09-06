---
title: An agent's Markdown is rendered by the client, so math survives in one surface and not another
tags: [agents, markdown, latex]
added: 2026-09-06
---

## Fact

The model emits plain text; whatever client displays the reply decides how it
renders. A terminal-style chat view renders GitHub-flavored Markdown with no math
extension, so `$x^2$` and `$$\frac{a}{b}$$` reach the reader as literal dollar
signs and backslashes. A phone or web chat client running a KaTeX/MathJax pass
over the same bytes shows a typeset formula.

Nothing in the reply distinguishes the two cases, and the model gets no rendered
view back — so the mismatch is invisible from the producing side until a human
says the output looks wrong.

## Why it matters

An answer built around notation degrades into noise on half the surfaces it can
be read on, and the failure is silent. It is worst for exactly the content that
needs notation most: derivations, formulas, matrices.

The same asymmetry hits tables, footnotes, nested HTML, and emoji-width
alignment — anything outside the Markdown core.

## How to apply

Write math for the surface actually in use, and switch when told:

- **No math renderer** — Unicode carries most of it: `x² + y² = r²`, `√2`, `π`,
  `≤`, `≠`, `α β`, `∑`. Put multi-step derivations in a fenced code block so
  spacing is preserved and nothing is reinterpreted.
- **Math renderer present** — LaTeX freely.
- **Files, not chat** — the file's own renderer decides, independently of the
  chat surface. GitHub `.md` renders `$…$`; a plain text editor does not.

Do not infer the surface from the model or the CLI name — the same session can be
read from several clients at once. Treat a reader's "this looks broken" as the
authoritative signal and restate the notation rather than re-sending it.
