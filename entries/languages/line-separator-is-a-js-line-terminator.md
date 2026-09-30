---
title: U+2028 and U+2029 end a JavaScript line comment and break a regex literal, though string literals accept them
tags: [javascript, unicode, parsing]
added: 2026-09-30
sources:
  - https://tc39.es/ecma262/#sec-line-terminators
  - https://github.com/tc39/proposal-json-superset
---

## Fact

LINE SEPARATOR (U+2028) and PARAGRAPH SEPARATOR (U+2029) are line terminators
in JavaScript source, exactly like `\n`. Since ES2019 they are allowed raw
inside string literals, but everywhere else they still end the line:

- In a regular expression literal, `/[<U+2028>]/` is a SyntaxError: "Invalid
  regular expression: missing /".
- In a `//` comment, everything after the character is code again:
  `let x = 1; // x<U+2028>x = 2;` runs `x = 2`.

Both characters are invisible in editors, diffs and terminals.

## Why it matters

They arrive by copy-paste from documents and web pages, and from tooling that
turns a `\u2028` escape into the raw character. The error points at a line
that looks complete, and the comment case is worse: no error at all, just a
statement that executes although it reads as commented out.

## How to apply

- Write these characters as escapes: `\u2028` inside a regex or string, or
  build the character class with `String.fromCharCode` / a code-point check.
- To find them: `grep -nP '[\x{2028}\x{2029}]' -r src/`.
- Code that filters them (sanitising names, for example) is safest as a
  code-point comparison rather than a regex containing them.
