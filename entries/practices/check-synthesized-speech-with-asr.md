---
title: Synthesized speech can be checked by transcribing it back, clip by clip and in the final mix
tags: [text-to-speech, speech-recognition, whisper, testing, audio]
added: 2026-11-27
sources:
  - https://huggingface.co/onnx-community/whisper-base.en
---

## Fact

A text-to-speech line that comes out garbled, mispronounced or swallowed reads
as fine in every log; only listening, or a speech recogniser, catches it.
Transcribing each generated clip with Whisper and taking the word error rate
against the intended text finds the bad lines; transcribing each line's span
cut out of the finished video, music and all, shows whether the mix masks it.

## Why it matters

Pitch-shifted, echoed or very short lines fail most, and they fail silently:
"Shiny, shiny" came out as "signy" in every voice tried, and an echo effect
turned a whole line into other words. Without the check, the first listener
finds them.

## How to apply

- Resample to 16 kHz, pad a tenth of a second each side, transcribe, and
  normalise case and punctuation before comparing words.
- Read the flagged list rather than gating on zero: interjections (ooh, arr,
  brr), homophones (isle and aisle) and invented names fail on every good take.
- Reword a line that fails in several voices; try another voice or less effect
  for one that fails in only one.
- Run the same check on the rendered mix; a line clean alone but not there
  needs louder speech or deeper ducking of the music under it.
