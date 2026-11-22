---
title: macOS sips crops and rotates the stored pixels and keeps the EXIF Orientation tag
tags: [macos, sips, images, exif]
added: 2026-11-23
sources:
  - https://exiftool.org/TagNames/EXIF.html
---

## Fact

`sips` ignores a JPEG's EXIF Orientation. `--cropOffset` counts stored pixels,
not the upright picture a viewer shows, and `--rotate` turns the stored pixels
while copying the tag unchanged. A phone photo saved landscape with
Orientation 6 ("turn 90° clockwise to show") therefore crops the wrong region,
and the output of `sips -r 90` is turned twice in every viewer that honours the
tag. `orientation` is not a sips property either: `sips -g orientation` prints
`<nil>` even when ImageIO reads 6 from the same file.

## Why it matters

Offsets measured on the photo as displayed land somewhere else, and a rotation
that put the pixels upright shows up sideways. Nothing warns, and the `<nil>`
reads like "no orientation set".

## How to apply

- Read the tag yourself: EXIF tag 0x0112 in IFD0 (1 upright, 6 turn 90° CW,
  8 turn 90° CCW, 3 turn 180°), or ImageIO's `kCGImagePropertyOrientation`.
- Map displayed coordinates to stored ones before cropping. For 6, displayed
  (X, Y) is stored (Y, H − X), H being the stored height.
- For an upright file, rotate the pixels as the tag says, then set the tag to 1
  (`exiftool -Orientation=1 -n`, or overwrite the two value bytes in place).
- Check a crop by looking at it, not by trusting the offsets.
