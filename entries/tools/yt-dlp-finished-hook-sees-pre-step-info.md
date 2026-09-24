---
title: yt-dlp's postprocessor "finished" hook sees the file from before the step ran
tags: [yt-dlp, python, hooks]
added: 2026-09-24
sources:
  - https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/postprocessor/common.py
---

## Fact

yt-dlp wraps every postprocessor's `run` so that it copies the info dict,
calls the `postprocessor_hooks` with `status: "started"`, runs the step, and
then calls them with `status: "finished"` — passing the same *copy* again. The
line that would pick up the step's returned info (`_, info = ret`) is never
used. So in the "finished" event of `ExtractAudio`, `info_dict["filepath"]`
still names the downloaded `.webm`, not the `.mp3` the step just wrote. The
new path first appears in the *next* step's "started" event.

## Why it matters

Anything keyed on a step's output — cleanup, progress display, moving the
file — silently acts on the old file. A cancel implemented by raising at the
first hook after the request (to stop a conversion that just finished) will
delete the source and leave the converted file behind, with no error.

## How to apply

- Read a step's output from the following step's "started" event; the final
  file is reported by the `MoveFiles` step, which always runs last.
- To stop a job from a hook, raise `yt_dlp.utils.DownloadCancelled` (yt-dlp
  re-raises it through its wrappers even with `ignoreerrors` on), and raise it
  from a "started" event, so the file to clean up is already known.
- A step running ffmpeg calls no hooks while it runs, so a cancel lands only
  when that step ends.
