# Conventions

## The bar for an entry

One entry holds **one durable, general fact**.

An entry belongs here only if every one of these is true:

- It is still true and useful **on a different machine**.
- It is still true and useful **on a different project**.
- It is still true and useful **in six months**.
- Someone who was not present when it was learned can act on it.

If any one fails, the knowledge is real but belongs elsewhere. Machine-specific
facts go in the personal global config. Project-specific facts go in that
project's own docs.

## What must never go in

- Absolute paths from a personal machine, usernames, home directories
- Names of private projects or repositories, internal URLs, ticket IDs
- Credentials, tokens, API keys, email addresses — under any circumstance
- Local port numbers, local environment variables, one-install tool paths
- Session narrative ("we tried X, then Y failed") — record the conclusion, not
  the story that produced it
- A restatement of official documentation that adds no insight

This repository is public. Treat every line as permanently published.

## Writing an entry

Path: `entries/<topic>/<kebab-case-slug>.md`

```markdown
---
title: Short declarative title
tags: [tag, tag]
added: YYYY-MM-DD
updated: YYYY-MM-DD   # only once it has actually been revised
sources:
  - https://example.com/where-this-was-confirmed
---

## Fact

The thing itself, stated plainly, in a sentence or two. A reader should be able
to stop here and still have gotten the point.

## Why it matters

The consequence of not knowing it. What breaks, what gets slow, what gets
misdesigned.

## How to apply

Concrete guidance. Code, a command, or a rule of thumb — whatever makes it
actionable.
```

Keep entries short. Roughly 40 lines is the ceiling; past that, the entry is
probably two facts and should be split.

State the fact in the title. `Gradle configuration cache breaks on Project access
at execution time` is a title. `Gradle notes` is not.

## Updating the index

`INDEX.md` is a table of contents with one line per topic index. Every entry
gets exactly one line in the index beside it, `entries/<topic>/INDEX.md`:

```markdown
- [Title](slug.md) — one-line summary. `tag`, `tag`
```

The link is relative to the index file, so it is just the entry's filename.
`practices` is indexed by subject instead: its line goes in the
`entries/practices/INDEX-<subject>.md` whose description in `INDEX.md` fits it,
or in `entries/practices/INDEX.md` when none does.

The summary is what a future agent uses to decide whether to open the file, so
write it for that decision and nothing else. The same goes for each topic's line
in `INDEX.md`: when a new entry falls outside what that line describes, widen
the description, or an agent looking for the entry will never open its index.

## Curating

**Prefer updating over adding.** Before writing a new entry, scan every topic
index that could already cover it. A near-duplicate is worse than no entry, because it splits the
knowledge across two files that will drift apart.

**Delete what turns out to be wrong.** Do not leave a correction sitting next to
a false claim; the false claim will be the part that gets read. Rewrite the entry
or remove it.

**Keep each index to one line per entry.** When a topic index grows past
roughly 150 lines, split it by subject, as `practices` is: move each large
subject into its own `entries/<topic>/INDEX-<subject>.md`, keep the rest in
`entries/<topic>/INDEX.md`, and give each file its own line in `INDEX.md`.

**Add a topic directory only when a third entry needs it.** Two related entries
live fine in an existing topic. Taxonomies that grow ahead of their contents rot.
