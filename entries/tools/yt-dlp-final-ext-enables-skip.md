---
title: yt-dlp re-encodes a file it already produced unless final_ext names the output
tags: [yt-dlp, media, python]
added: 2026-09-01
sources:
  - https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py
---

## Fact

Before downloading, yt-dlp checks whether the target file is already on disk.
With a converting postprocessor in play (`FFmpegExtractAudio`,
`FFmpegVideoConvertor`) the name it downloads to is not the name it finishes
with, so the check maps one to the other through `params['final_ext']`.

The command line sets `final_ext` itself from `--audio-format` /
`--recode-video`. A library caller passing the postprocessor in
`YoutubeDL(...)` options gets no such default, so the finished file is never
recognised: every run downloads the source again and re-encodes it, producing
a byte-identical result.

`__real_download` does not reveal this either. It sits on each entry of
`requested_downloads`, not on the video info dict, and yt-dlp leaves it unset
on the reuse path — a progress hook that records which IDs actually reached
`status == "finished"` is the reliable witness.

## Why it matters

Nothing fails and nothing warns. The only symptoms are runtime and bandwidth,
which look like normal cost for the work, so a batch job can re-fetch and
re-encode its whole library on every run without anyone noticing.

## How to apply

Set `final_ext` to the extension the file will actually carry — which is not
always the codec name:

```python
FINAL_EXT = {"mp3": "mp3", "aac": "m4a", "m4a": "m4a", "opus": "opus",
             "vorbis": "ogg", "flac": "flac", "alac": "m4a", "wav": "wav"}
ydl_opts["final_ext"] = FINAL_EXT[codec]
```

The authoritative mapping is `yt_dlp.postprocessor.ffmpeg.ACODECS`, whose values
are `(extension, encoder, extra_args)`. Verify a fix by file mtime, not by
wall-clock time: a skipped run and a cached-network run look alike.
