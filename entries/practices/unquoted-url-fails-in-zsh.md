---
title: An unquoted URL with `?` fails in zsh before the command runs, though bash passes it through
tags: [shell, zsh, cli, documentation]
added: 2026-09-23
sources:
  - https://zsh.sourceforge.io/Doc/Release/Options.html#index-NOMATCH
  - https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html
  - https://github.com/ohmyzsh/ohmyzsh/blob/master/lib/misc.zsh
---

## Fact

`?` is a glob character. When a word containing one matches no file, zsh's
default `NOMATCH` option aborts the whole line with
`zsh: no matches found: <word>`, and the program never starts. bash's defaults
(`failglob` and `nullglob` both off) pass the word through unchanged, so the
same line works there.

Oh My Zsh blurs the line further: unless `DISABLE_MAGIC_FUNCTIONS=true`, it
turns on `url-quote-magic`, which escapes URL characters as they are typed or
pasted. The same paste works in an Oh My Zsh shell and fails in a plain one,
including the stock macOS shell.

## Why it matters

The error names the URL, so it reads as the tool rejecting the link, when the
tool was never invoked. Docs checked in bash or Oh My Zsh pass review and fail
for plain-zsh users. Even in bash the line is only accidentally right: an `&`,
as in `watch?v=ID&list=PL`, ends the command there, runs it in the background,
and silently drops the rest of the URL — in every shell.

## How to apply

- Quote every URL in published command examples, placeholders included:
  `tool "URL"`, so a link pasted over the placeholder lands inside quotes.
- A user hitting it: quote the URL. `noglob tool …` also gets past the `?`, but
  not the `&`; `setopt no_nomatch` only hides the problem.
- On `no matches found`, check the shell before debugging the program: nothing
  ran.
