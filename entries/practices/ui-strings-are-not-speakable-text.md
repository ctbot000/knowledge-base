---
title: A UI string is not speakable text — emoji get names, and a stripped operator changes the sentence
tags: [web-speech, unicode, i18n, frontend]
added: 2026-09-16
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/text
  - https://www.unicode.org/charts/
---

## Fact

Text written to be read by eye carries decoration that a speech engine reads
literally. Emoji are not silent: most engines announce them by their Unicode
name, so a cheerful "Correct! 🎉" is spoken "Correct, party popper".

Stripping the decoration introduces the second half of the problem. The
arrows-and-symbols range `U+2190–U+2BFF` — the obvious sweep for dingbats, arrows
and game glyphs — also contains `U+2212 MINUS SIGN`, the typographic minus a
designer actually used. A blunt strip turns "(7 + 7) × 2 − 4 = 24" into
"7 plus 7 2 4 equals 24": still fluent, and now false.

## Why it matters

Screen text and spoken text are the same string in the source, so nothing looks
wrong in review, in a diff, or in a test that asserts on the DOM. The defect
exists only in the audio, and only whoever listens to that particular string
ever meets it.

Numbers are where it bites hardest. A dropped emoji is merely odd; a dropped
operator yields a confident, wrong sentence — worst of all in anything
teaching arithmetic or reading.

## How to apply

- Convert before you strip: `× ÷ − + =` become "times", "divided by", "minus",
  "plus", "equals". Only then remove whatever symbols remain.
- Strip emoji by range: `U+1F000–U+1FAFF`, plus `U+FE0F` variation selectors and
  `U+20E3` keycaps, which otherwise linger after the base character goes.
- Map em and en dashes to a comma; they are pauses in print and nothing at all
  in speech.
- Run every string in the corpus through the transform and assert on the result
  — flag any that comes out empty or still holds a non-ASCII character. Spot
  checks miss exactly the one string with the unusual glyph.
