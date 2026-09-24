---
title: A yt-dlp section download gets the same file name as the whole video
tags: [yt-dlp, ffmpeg, audio]
added: 2026-09-24
sources:
  - https://github.com/yt-dlp/yt-dlp#output-template
---

## Fact

`--download-sections` (API: `download_ranges`) changes what is downloaded but
not what the file is called: the default template
`%(title)s [%(id)s].%(ext)s` has no field that varies with the section. Before
downloading, yt-dlp checks whether the target file exists and, when it does,
reports "has already been downloaded" and returns it. A 15-second clip and the
full track therefore satisfy each other: whichever was fetched first comes
back for the other request.

## Why it matters

Nothing warns. A request for the full album track returns the 15-second clip
from an earlier run — with a success status and the right title — and the
mistake surfaces only when someone plays the file.

## How to apply

Put the range in the name whenever a section is requested, e.g. build
`%(title)s [%(id)s] [0m05s-0m20s].%(ext)s` from the requested start and end,
or use the section fields yt-dlp fills in for the output template
(`%(section_start)s`, `%(section_end)s`). Keep the plain name for the full
download so an earlier full file is still reused.
