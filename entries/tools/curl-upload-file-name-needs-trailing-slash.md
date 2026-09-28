---
title: curl -T appends the local file name only to a URL ending in a slash, so a query string turns it off
tags: [curl, http, cli, documentation]
added: 2026-09-28
sources:
  - https://curl.se/docs/manpage.html#-T
---

## Fact

`curl -T photo.jpg https://host/` uploads to `/photo.jpg`: when the URL has no
file part, curl appends the local file name. Add a query string and it stops:
`curl -T photo.jpg "https://host/?expires=1h"` sends `PUT /?expires=1h`, so the
server never learns the name. Checked with curl 8.7.

## Why it matters

Upload services in the transfer.sh style take the file name from the path.
Documentation that shows options as query parameters on the bare URL produces
unnamed uploads (`upload.bin`, `paste.txt`) with no error on either side.

## How to apply

- Put options in request headers, e.g. `curl -T file -H 'X-Expires: 1h' https://host/`.
- Or spell the name out: `curl -T file "https://host/file.txt?expires=1h"`.
- Check which request line curl really sends with `curl -v` before documenting
  an upload command.
