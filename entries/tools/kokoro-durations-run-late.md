---
title: Kokoro's own phoneme durations run late against its audio, so lip sync built on them lags
tags: [text-to-speech, kokoro, lip-sync, alignment, audio]
added: 2026-11-26
sources:
  - https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX-timestamped
---

## Fact

The timestamped export of the Kokoro speech model returns one duration per input
token (units of 600 samples, 25 ms at 24 kHz, rounded, at least one). Summed up,
they place sounds later than the audio does: on 1,773 clips of one voice,
realigned with a model trained on them, sounds began 74 ms earlier on average.

- A vowel or sonorant starts about 25 to 40 ms before its token.
- A stop's token starts near its burst, so its closure is 70 to 80 ms earlier.
- The first sound begins inside the leading padding token (often 100 ms or more
  early) and the last one ends inside the trailing padding.
- Stress marks are tokens with durations of their own, two or three units, that
  are really part of the consonant before and the vowel after.

## Why it matters

A mouth driven straight from these numbers closes for `p` after the sound has
already stopped. The error is constant enough to look like output latency and
get tuned away, which then breaks every other voice source.

## How to apply

- For prepared clips, force-align instead: monophone HMMs trained on a few
  hundred of the model's own clips, started from its durations, settle in six
  passes. Pull boundaries towards the durations, shifted, or they drift.
- Live, shift starts by -35 ms (stops -70 ms), take the first start and the last
  end from the signal's level, and find bursts as the sharpest high-band rise.
- A lone phoneme is often said as a different sound, vowels above all (a lone
  `ɪ` measured as a back vowel): cut it out of a carrier such as `hˈɪd`, and
  check it by formants.
