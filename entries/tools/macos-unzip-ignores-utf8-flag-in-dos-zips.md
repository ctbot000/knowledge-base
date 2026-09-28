---
title: macOS's unzip decodes names in a ZIP "made by" MS-DOS as code page 437, even with the UTF-8 flag set
tags: [zip, unicode, macos]
added: 2026-09-28
sources:
  - https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
---

## Fact

The `unzip` that ships with macOS (Info-ZIP UnZip 6.00, Apple build) ignores
general-purpose flag bit 11 ("names are UTF-8") when an entry's *version made by*
host byte is 0, MS-DOS. It converts the name from code page 437 instead, so a
UTF-8 name comes out as `??????`, and on APFS, which rejects the resulting bytes,
extraction fails with `write error (disk full?)`. Python's `zipfile`, `ditto`
(Archive Utility) and `bsdtar` honour the flag and extract the same archive
correctly, and `unzip -t` reports it as fine.

## Why it matters

A hand-written ZIP writer usually copies the minimal DOS header layout and sets
bit 11, which passes every check except extraction in a terminal. The error then
points at disk space rather than at file names.

## How to apply

- Write *version made by* as Unix: high byte 3, e.g. `0x0314`.
- Then set Unix permissions in the upper 16 bits of the external file
  attributes, e.g. `(0o100644 << 16) >>> 0`. With Unix origin and attributes 0,
  `unzip` extracts every file with mode `000`.
- Test with a real extraction (`unzip -d out archive.zip`) on macOS, not only
  with `unzip -t`.
