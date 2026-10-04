---
title: A \uXXXX escape in a Claude Code tool call reaches the tool as the raw character
tags: [claude-code, unicode, agents]
added: 2026-10-04
updated: 2026-10-04
---

## Fact

A `\uXXXX` (four hex digits) written in any tool call argument, Bash, Write and
Edit alike, arrives at the tool already decoded: `printf '%s' 'x\u200dy'`
prints a raw U+200D. Only that form is decoded, and only once: `\\` stays two
backslashes and `\u{200d}` stays text. Edit adds a fallback on top: when
`old_string` matches only after turning characters back into escapes, it does
the same to `new_string`, so its Hangul and emoji land as `\u` escapes.

## Why it matters

Source that names an invisible character by escape (a regex exempting
zero-width joiners, a test feeding in a zero-width space) gets the invisible
character itself, with every tool reporting success; later edits then fail to
match it. Both forms run the same, so tests rarely notice.

## How to apply

- To write the six characters `\u200d`, escape the backslash itself:
  `\u005cu200d` decodes once to `\u200d`.
- Or keep four-digit escapes out of literals: `String.fromCharCode(0x200b)`,
  `String.fromCodePoint(0x1f468, 0x200d, 0x1f469)`, the braced `\u{200d}` in
  JavaScript, `\x{200d}` in Perl.
- After any change involving escapes, check the bytes, not the rendered text:
  `od -c` on the line, or
  `perl -CSD -ne '$n++ while /[\x{200b}-\x{200f}]/g; END { print $n+0 }' file`.
