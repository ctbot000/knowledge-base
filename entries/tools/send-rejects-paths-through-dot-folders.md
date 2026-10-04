---
title: send answers 404 for a file whose absolute path runs through a dot-folder
tags: [node, http, static-files, express]
added: 2026-10-05
sources:
  - https://github.com/pillarjs/send#dotfiles
  - https://expressjs.com/en/api.html#res.sendFile
---

## Fact

The `send` package checks every segment of the path it is given, and its
default `dotfiles: 'ignore'` answers 404 when any segment starts with a dot.
Given an absolute path and no `root`, those segments include the folders above
the file, so a file under `~/.myapp/` is "not found" although it exists.
Express's `res.sendFile(absolutePath)` goes through `send` and does the same.

## Why it matters

App data often lives in a dot-folder (`~/.config/…`, `~/.myapp`), and the
failure looks like a missing file rather than a setting. Tests usually keep
their data in a temp folder without a dot, so they pass while the real install
answers 404.

## How to apply

- Pass the folder as `root` and only the file name as the path; only segments
  below `root` are checked:

  ```js
  send(req, `/${encodeURIComponent(basename(file))}`, { root: dirname(file) }).pipe(res);
  // Express: res.sendFile(basename(file), { root: dirname(file) })
  ```

- Do not fix it with `dotfiles: 'allow'`, which also serves dotfiles inside the
  folder.
- Give a test's data folder a dot-folder in its path, as the real one has.
