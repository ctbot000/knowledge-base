---
title: Browsers break Korean text between any two syllables unless word-break is keep-all
tags: [css, typography, korean]
added: 2026-09-29
sources:
  - https://www.unicode.org/reports/tr14/#LB27
  - https://www.w3.org/TR/css-text-3/#word-break-property
---

## Fact

Line breaking treats a Hangul syllable like a Chinese character (UAX #14 rule
LB27), so under the default `word-break: normal` a line may end between any two
syllables: 어린이 can wrap as 어 / 린이. Korean, unlike Chinese and Japanese,
puts spaces between words, and `word-break: keep-all` limits breaks to those
spaces and to punctuation. English wrapping is unchanged by it.

## Why it matters

The split depends on the width, so a page that looks right on a desktop breaks
words apart on a phone, in a card or in a table cell — and only on whichever
line happens to end mid-word. Korean readers see it as a broken layout, the way
an English reader would see "dictio / nary" with no hyphen.

## How to apply

```css
body {
  word-break: keep-all;       /* Korean wraps at spaces, like English */
  overflow-wrap: break-word;  /* a run longer than the line may still break */
}
```

- Always pair it with `overflow-wrap`: `keep-all` alone lets a long run with no
  space, such as a URL, overflow its box.
- Keep it off Chinese and Japanese. They have no spaces, so `keep-all` leaves
  only punctuation to break at and whole clauses overflow. On a page that mixes
  them, scope it with `:lang(ko)`.
