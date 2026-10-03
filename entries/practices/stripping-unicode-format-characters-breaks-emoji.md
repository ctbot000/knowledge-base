---
title: Stripping invisible characters (\p{C}) from text splits emoji built with joiners and tags
tags: [unicode, emoji, sanitization]
added: 2026-10-03
sources:
  - https://unicode.org/reports/tr51/#Emoji_ZWJ_Sequences
  - https://unicode.org/reports/tr51/#valid-emoji-tag-sequences
---

## Fact

Several emoji are sequences held together by format characters, category
Cf: the zero width joiner U+200D in 👨‍👩‍👧 or 🧑‍💻, and the tag characters
U+E0020 to U+E007F that turn 🏴 into the flags of England, Scotland and
Wales. A sanitizer that deletes `\p{C}` (or `\p{Cf}`) to remove invisible or
bidirectional-override characters deletes these too, and the emoji fall
apart into their parts or a plain black flag.

## Why it matters

Chat messages, names and comments come out subtly mangled for emoji users,
with no error, and tests written with plain emoji like 😀 (one code point)
still pass.

## How to apply

- Exempt them when stripping: in JavaScript,
  `text.replace(/(?![‍\u{e0020}-\u{e007f}])\p{C}/gu, '')`.
  Variation selectors (U+FE0F) and skin-tone modifiers are not in `\p{C}`
  and survive anyway.
- For identifiers that must not look alike (usernames), refusing all of
  `\p{C}` is still reasonable: that rejects such emoji rather than
  corrupting them.
- Test with a ZWJ family emoji and a subdivision flag, not only single
  code-point emoji.
