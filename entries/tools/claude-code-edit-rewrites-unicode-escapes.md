---
title: Claude Code's Edit and Write tools can swap \u escapes and the characters they stand for
tags: [claude-code, unicode, editing]
added: 2026-10-04
---

## Fact

When Claude Code's Edit or Write tool handles text containing `\uXXXX`
escapes, it may convert between an escape and its literal character: a
`\u200d` typed in `new_string` can land in the file as a raw, invisible
U+200D, and when `old_string` held an escape, non-ASCII literals in
`new_string` (Hangul, emoji) can land as `\u` escapes instead. The tool
reports success either way. Write does the first with its `content` too.

## Why it matters

Source that deliberately names an invisible character by escape (a regex
exempting zero-width joiners, a test feeding in a zero-width space) silently
turns into an invisible literal that reviews cannot see and later edits cannot
match. The reverse turns readable test strings into opaque escapes. Both still
run, so tests rarely catch it.

## How to apply

- After an edit whose text involves `\u` escapes, check the bytes, not the
  rendered view: `od -c` on the line, or count with
  `perl -CSD -ne '$n++ while /[\x{200b}-\x{200f}]/g; END { print $n+0 }' file`.
- In new code, build invisible characters at run time instead of escaping them
  in a string literal: `String.fromCharCode(0x200b)`,
  `String.fromCodePoint(0x1f468, 0x200d, 0x1f469)`.
- To insert or repair escapes exactly, use a byte-faithful tool such as
  `perl -CSD -i -pe` or `sed`, then re-check.
