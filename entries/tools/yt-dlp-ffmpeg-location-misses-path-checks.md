---
title: yt-dlp's ffmpeg_location does not reach its own partial-download check
tags: [yt-dlp, media, ffmpeg]
added: 2026-09-01
sources:
  - https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py
---

## Fact

`--ffmpeg-location` (option `ffmpeg_location`) is honoured by yt-dlp's
postprocessors, but not by every internal availability check. The guard for
section downloads — `--download-sections`, or `download_ranges` in the API —
calls `FFmpegFD.available()` with no downloader attached, so the probe it
performs can only search `PATH`.

With ffmpeg installed somewhere off `PATH` and pointed at correctly, conversion
and tagging work while a trimmed download dies on:

```
ERROR: You have requested downloading the video partially,
but ffmpeg is not installed. Aborting
```

The message is wrong twice over: ffmpeg is installed, and yt-dlp has been told
where it is.

## Why it matters

The error names the one thing the operator already handled, so the search goes
to the ffmpeg install and the flag's spelling rather than to the lookup path.
It bites hardest where ffmpeg deliberately lives outside `PATH` — a vendored
binary, a per-project virtualenv, a locked-down image.

## How to apply

Prepend the directory to `PATH` in the process rather than relying on the
option alone; the option can stay for the postprocessors.

```python
os.environ["PATH"] = os.pathsep.join([str(ffmpeg_dir), os.environ.get("PATH", "")])
```

The binary must be named `ffmpeg` — yt-dlp matches on basename, so a versioned
filename needs a symlink. Note also that `ffprobe` is a separate lookup:
cover-art embedding needs it and raises a fatal postprocessing error without
it, even when ffmpeg itself is found.
