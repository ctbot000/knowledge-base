---
title: Speech synthesis picks a voice by locale, not by the language of the text
tags: [web-speech, i18n, browser, frontend]
added: 2026-09-02
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/lang
  - https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/getVoices
---

## Fact

A `SpeechSynthesisUtterance` with no `lang` and no `voice` inherits the language
of the document — and failing that, the host's default voice. Nothing inspects
the string being spoken. So English text handed to a browser on a non-English
system is read aloud by a voice for that system's locale, which pronounces it
with that language's phonetics and produces something the listener cannot parse
as English at all.

The obvious fix is half a fix, because `speechSynthesis.getVoices()` returns an
empty array on first call in most browsers. The list is populated
asynchronously and announced by a `voiceschanged` event, so voice selection
written inline at startup silently finds nothing and falls back to the default.

## Why it matters

The failure is invisible to a developer on an English-locale machine: the
default voice is already English and everything sounds correct. It appears only
for users elsewhere, and it degrades to gibberish rather than to silence — so it
reads as a broken audio feature rather than a missing two-line configuration.

Speech is also usually the accessibility or attention-getting path, which makes
it exactly the feature that must not quietly fail for part of the audience.

## How to apply

- Always set `utterance.lang` explicitly to the language of the string.
- Select a matching voice rather than trusting `lang` alone; some engines honour
  the tag only when a voice for it exists:
  `voices.filter(v => /^en\b|^en-/i.test(v.lang))`, preferring `localService`.
- Seed the voice list at startup and refresh it:
  `speechSynthesis.addEventListener('voiceschanged', loadVoices)`.
- Call `speechSynthesis.cancel()` before `speak()`; utterances queue rather than
  replace, so a repeated alert otherwise stacks up a backlog.
