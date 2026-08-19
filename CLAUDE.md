# Operating instructions

This repository is a knowledge base read by AI coding agents at the start of
every session. Its value depends entirely on the signal-to-noise ratio of
`INDEX.md`, so the curation rules matter more here than the writing does.

Read [CONVENTIONS.md](CONVENTIONS.md) before adding or editing an entry. The
rules that get broken most often:

1. **Generality.** An entry must hold on a different machine, on a different
   project, in six months. No local paths, no private project names, no
   credentials. This repository is public.
2. **One fact per entry.** If the title needs an "and", it is two entries.
3. **Update before you add.** Scan the index first. A near-duplicate splits
   knowledge across two files that will drift.
4. **Index every entry, once.** One line, written to help a future agent decide
   whether to open the file.

## Adding an entry

1. Scan `INDEX.md` for existing coverage.
2. Write or revise `entries/<topic>/<slug>.md` using the template in
   `CONVENTIONS.md`.
3. Add or update its line in `INDEX.md`.
4. Commit both together, with a message naming the fact rather than the file.

## What not to do here

Do not add an entry to record that a task happened, to summarize a session, or
to restate documentation. Do not pad the index to make the repository look
fuller — an index of ten entries that are all worth reading beats fifty where
most are not.
