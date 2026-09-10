---
title: A regenerate-and-commit job must produce output that is a pure function of its input
tags: [automation, ci, code-generation]
added: 2026-09-10
---

## Fact

A scheduled job that regenerates a file and commits it when the file changed
only stays quiet if the generator is deterministic with respect to its
*upstream* input. A build timestamp — `Generated at 2026-09-10 14:22` — makes
every byte of the output a function of the clock as well, so the diff is never
empty and the job commits on every tick.

The same applies to any incidental non-determinism: an unsorted dict or set
iteration, a random id, a locale-dependent format.

## Why it matters

The failure is not loud. The job works, the site is correct, and the only
symptom is a commit history filling with identical-looking commits — which then
makes the real change, the one that added a new entry, impossible to find. It
also defeats the `git diff --quiet` guard people reach for to keep the job
cheap, so every run pushes and every push re-triggers downstream builds.

## How to apply

- Derive any displayed "freshness" from the data, not from the clock: the newest
  `updated_at` across the fetched records says something true and changes only
  when the records do.
- Sort every collection before rendering it.
- Guard the commit on content, and let an unchanged run be a no-op:

  ```sh
  git diff --quiet -- out.html && { echo "No change."; exit 0; }
  ```

- Test it by running the generator twice with no upstream change and diffing;
  identical output is the contract.
