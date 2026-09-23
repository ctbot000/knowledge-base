# Operating instructions

This repository is a knowledge base read by AI coding agents at the start of
every session. Its value depends entirely on the signal-to-noise ratio of its
indexes — `INDEX.md` and the topic indexes it links — so the curation rules
matter more here than the writing does.

Read [CONVENTIONS.md](CONVENTIONS.md) before adding or editing an entry. The
rules that get broken most often:

1. **Generality.** An entry must hold on a different machine, on a different
   project, in six months. No local paths, no private project names, no
   credentials. This repository is public.
2. **One fact per entry.** If the title needs an "and", it is two entries.
3. **Update before you add.** Scan the topic indexes first. A near-duplicate
   splits knowledge across two files that will drift.
4. **Index every entry, once.** One line in the topic index beside it, written
   to help a future agent decide whether to open the file.

## Adding an entry

1. Scan the topic indexes that `INDEX.md` points to for existing coverage.
2. Write or revise `entries/<topic>/<slug>.md` using the template in
   `CONVENTIONS.md`.
3. Add or update its line in the index beside it: `entries/<topic>/INDEX.md`,
   or for `practices` the `INDEX-<subject>.md` that fits. `INDEX.md` itself
   changes only when a topic's description there no longer covers the entry.
4. Commit them together, with a message naming the fact rather than the file.

## What not to do here

Do not add an entry to record that a task happened, to summarize a session, or
to restate documentation. Do not pad the index to make the repository look
fuller — an index of ten entries that are all worth reading beats fifty where
most are not.
