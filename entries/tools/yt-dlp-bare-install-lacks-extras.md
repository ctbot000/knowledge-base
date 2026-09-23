---
title: A bare `pip install yt-dlp` lacks mutagen and the YouTube challenge solver
tags: [yt-dlp, python, packaging]
added: 2026-09-23
sources:
  - https://github.com/yt-dlp/yt-dlp/wiki/EJS
  - https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/postprocessor/embedthumbnail.py
---

## Fact

Every dependency of the `yt-dlp` package sits behind an extra; the bare
install pulls in nothing. `yt-dlp[default]` adds, among others, `mutagen` and
`yt-dlp-ejs`, and two features fail without them:

- **Cover art in ogg, opus and flac** is written only through mutagen. Without
  it, the thumbnail step raises `module mutagen was not found` and the whole
  video counts as failed. mp3 and m4a embed through ffmpeg, so a test on mp3
  passes.
- **YouTube's JavaScript challenge** needs a runtime (Deno by default) *and*
  the solver script from `yt-dlp-ejs`. Installing Deno alone swaps the "No
  supported JavaScript runtime" warning for "challenge solver script ... were
  skipped" and "n challenge solving failed: Some formats may be missing".

## Why it matters

Both look like environment trouble rather than a packaging gap, and the usual
fix (install mutagen, install Deno) each solves half of the problem.

## How to apply

- Depend on `yt-dlp[default]`, never bare `yt-dlp`, in a project that embeds
  it. `yt-dlp[default,deno]` also brings Deno through pip.
- Without the extra, `--remote-components ejs:github` downloads the solver at
  run time.
- Confirm with a metadata-only run (`yt-dlp -s URL`): no `[jsc]` or
  `n challenge` lines means the challenge was solved.
