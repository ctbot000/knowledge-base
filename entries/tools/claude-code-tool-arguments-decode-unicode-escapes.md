---
title: A \uXXXX escape in a Claude Code tool call reaches the tool as the raw character
tags: [claude-code, unicode, agents]
added: 2026-10-04
updated: 2026-10-04
sources:
  - https://github.com/anthropics/claude-code/issues/72957
  - https://github.com/anthropics/claude-code/issues/99361
---

## Fact

Claude Code runs a repair pass over every tool call's input (Bash, Write, Edit
and MCP alike) that decodes `\uXXXX` (four hex digits) into the character:
`printf '%s' 'x\u200dy'` prints a raw U+200D. It decodes once, keeps
`\\u200d`, lone surrogates, control characters and `\u{200d}` as
typed, and skips a whole string that holds anything path-like: a drive letter
(`C:\`) or a quote, two backslashes, text and a backslash, as in
`"\\u200b";\n`. Edit then adds a fallback: when `old_string` matches only in
escaped form, every non-ASCII character in `new_string` is written as an escape,
Hangul and emoji included.

## Why it matters

Source that names an invisible character by escape (a regex exempting joiners, a
test feeding in a zero-width space) gets the invisible character itself, with
every tool reporting success. Whether a given escape survives depends on
unrelated text elsewhere in the same input, so a check that passed once proves
nothing.

## How to apply

- Build such characters at run time instead: `String.fromCharCode(0x200b)`,
  `String.fromCodePoint(0x1f468, 0x200d, 0x1f469)`, `\x{200d}` in Perl.
- For escape text in a file, type a placeholder such as `@@BS@@` for each backslash and swap it in with a script
  (`perl -pi -e 's/\@\@BS\@\@/\x5c/g'`); `\u005cu200b` gives `\u200b`
  only while the pass runs.
- Anchor an Edit on text without escapes, so the exact match wins.
- Check the bytes after any such change: `od -c`, or count
  `[\x{200b}-\x{200f}]` with `perl -CSD`.
