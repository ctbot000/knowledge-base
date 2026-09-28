---
title: In zsh, an unquoted word starting with = is replaced by the path of a command
tags: [shell, zsh, cli]
added: 2026-09-28
sources:
  - https://zsh.sourceforge.io/Doc/Release/Expansion.html
  - https://zsh.sourceforge.io/Doc/Release/Options.html#index-EQUALS
---

## Fact

With the `EQUALS` option, which is on by default, zsh expands `=name` at the
start of a word to the full path of the command `name`: `echo =ls` prints
`/bin/ls`. So a separator such as `echo =====` looks up a command called `====`
and aborts the line with `zsh: ==== not found`. bash prints the equals signs.

## Why it matters

Scripts and one-liners written against bash fail under zsh, the default shell
on macOS, as soon as they print a banner (`echo ======`) or pass a bare
`=value` argument, and the error names neither the option nor the expansion.
Output printed after the failing `echo` in the same `&&` chain never appears.

## How to apply

- Quote such words: `echo '====='`, `printf '%s\n' '=value'`.
- In zsh scripts that must pass `=word` arguments unquoted, `setopt no_equals`.
- A `not found` naming a string of `=` signs is this expansion, not a missing
  program. See also [[unquoted-url-fails-in-zsh]].
