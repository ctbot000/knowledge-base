---
title: yt-dlp's `--audio-format alac` writes lossy AAC
tags: [yt-dlp, ffmpeg, audio]
added: 2026-09-23
sources:
  - https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/postprocessor/ffmpeg.py
---

## Fact

When `FFmpegExtractAudioPP` re-encodes, it replaces the codec's own ffmpeg
options with the quality arguments (`more_opts = self._quality_args(acodec)`).
ALAC is the one codec whose encoder lives only in those options —
`'alac': ('m4a', None, ('-acodec', 'alac'))` — so ffmpeg is handed no codec at
all and picks the `.m4a` default: AAC. The file gets the extension ALAC would
have, and nothing warns. The same line drops `-f adts` for `aac`, which then
comes out as MP4 rather than raw ADTS.

Present in yt-dlp 2026.08.19 and on master as of 2026-09-23.

## Why it matters

The failure is silent: someone asking for lossless audio gets lossy audio
with a plausible file name, and only a codec probe tells them apart.

## How to apply

Pass the encoder again as output arguments for the extract step; they are
appended after yt-dlp's own, so they win, and they stay harmless once the bug
is fixed:

```bash
yt-dlp -x --audio-format alac --ppa "ExtractAudio+ffmpeg_o:-acodec alac" URL
```

In the Python API: `postprocessor_args={"extractaudio+ffmpeg_o": ["-acodec", "alac"]}`.
Check lossless output by codec, never by extension:
`ffprobe -v error -show_entries stream=codec_name -of csv=p=0 FILE`.
