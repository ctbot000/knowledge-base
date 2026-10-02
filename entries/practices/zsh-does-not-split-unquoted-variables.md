---
title: zsh does not split an unquoted $VAR into words, so a variable holding several arguments passes them as one
tags: [shell, zsh, cli]
added: 2026-10-02
sources:
  - https://zsh.sourceforge.io/Doc/Release/Options.html
  - https://zsh.sourceforge.io/FAQ/zshfaq03.html
---

## Fact

With the `SH_WORD_SPLIT` option off, as it is by default, zsh expands an
unquoted `$VAR` to a single word. After `SIZES="800x600 1024x768"`, the
command `prog $SIZES` gets one argument, `800x600 1024x768`; bash, and zsh
in `sh` emulation, split it into two.

## Why it matters

Nothing fails in the shell. The program receives one argument where it
expected a list, and the error surfaces inside it, far from the cause: a
parse that yields `NaN`, a lookup of a file named with spaces, a loop that
runs once. One-liners and scripts written for bash break this way under zsh,
the default shell on macOS.

## How to apply

- Keep lists in arrays, which expand the same in bash and zsh:
  `sizes=(800x600 1024x768); prog "${sizes[@]}"`.
- In zsh only, `${=VAR}` splits one expansion, or `setopt sh_word_split`
  splits them all; or run the script with bash explicitly.
- See also [[zsh-equals-word-is-a-command-lookup]] and
  [[unquoted-url-fails-in-zsh]].
