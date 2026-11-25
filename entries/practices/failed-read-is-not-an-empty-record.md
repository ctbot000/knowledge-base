---
title: A read-modify-write that takes any failed read for an empty record writes the loss over the data
tags: [error-handling, data-loss, files, storage]
added: 2026-11-25
---

## Fact

A helper that returns null whenever a file cannot be read or parsed, followed
by `?? {}`, an edit and a write, replaces the record with the edit alone the
first time a read fails for any reason: a damaged file, a permission change,
too many open files. Only "there is no such file" means an empty record.

## Why it matters

The read error was passing and would have gone away; the write makes it
permanent. Nothing is logged, and the record still looks valid, only nearly
empty. The same helper is harmless for display or for data another copy will
refill, which is how it comes to be used where the file is the only copy.

## How to apply

- Treat only the not-found error as empty (`ENOENT`, 404, zero rows) and let
  every other error, a parse error included, fail the operation.

  ```js
  try {
    record = JSON.parse(await readFile(file, 'utf8'));
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  ```

- Keep the caller's change somewhere until the write succeeds (a queue on the
  client, a retry), so that failing loudly loses nothing either.
- In a move or merge of several records, read all of them before changing any.
- Ask it of data that moves from many copies to one: a tolerant reader that was
  fine for a cache or a backup is not fine for the only copy.
- Test it: damage the file, attempt the write, and assert that it fails and the
  file's bytes are unchanged.
