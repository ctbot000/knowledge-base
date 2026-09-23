---
title: Homebrew's ffmpeg formula has no libvorbis, and ffmpeg-full is keg-only
tags: [homebrew, ffmpeg, audio]
added: 2026-09-23
sources:
  - https://formulae.brew.sh/formula/ffmpeg
  - https://formulae.brew.sh/formula/ffmpeg-full
---

## Fact

Homebrew's `ffmpeg` formula is a slim build; the optional libraries moved to
`ffmpeg-full`, and `libvorbis` is one of them. The slim build still lists an
encoder named `vorbis` — ffmpeg's native, experimental one — so a glance at
`ffmpeg -encoders` looks fine, but anything that asks for `libvorbis` by name
fails with `Encoder not found`. yt-dlp's `--audio-format vorbis` does exactly
that, after downloading the whole source.

`ffmpeg-full` is keg-only: installing it puts nothing on `PATH`.

## Why it matters

The error arrives at the end of a download and names neither the missing
library nor the formula split, and the obvious fix — `brew install
ffmpeg-full` — appears not to work because the old binary still answers.

## How to apply

- Check for the exact encoder name before a long job:
  `ffmpeg -hide_banner -encoders | grep -w libvorbis`
- Use the full build explicitly: `"$(brew --prefix ffmpeg-full)/bin/ffmpeg"`,
  or hand that directory to the tool (yt-dlp: `--ffmpeg-location`).
- Or prefer Opus, Vorbis's successor, which the slim formula supports.
