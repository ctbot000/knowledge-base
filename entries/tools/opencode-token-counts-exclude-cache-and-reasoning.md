---
title: OpenCode's per-message token counts exclude cache reads from input and reasoning from output
tags: [opencode, tokens, sqlite, cost]
added: 2026-10-13
---

## Fact

OpenCode (v2) stores sessions in a SQLite file, `opencode.db` under its data
directory (`~/.local/share/opencode` on Linux and macOS), not in JSONL. Each
model step is one `session_message` row with `type = 'assistant'`, whose JSON
`data` holds `tokens: {input, output, reasoning, cache: {read, write}}`.
`input` is uncached input only and `output` excludes `reasoning`, so the four
buckets are disjoint. `cost` is 0 for subscription providers.

## Why it matters

Adding `cache.read` to `input` as if it were a subset, or reading `output` as
the billed output, undercounts reasoning models: a step can show output 68
beside reasoning 232. Summing `session_v2`'s per-session totals instead of the
rows also drifts, because those include aborted steps whose rows carry no
`tokens` at all. A tool that runs a model is not its provider, either: Claude
Code can point at a GLM endpoint and OpenCode can drive Claude.

## How to apply

- Bill `input` at the input rate, `output + reasoning` at the output rate and
  `cache.read` at the provider's cached-input rate, which is not always a fixed
  fraction of input (GLM's is not).
- Open the file read-only (`file:…?mode=ro` as a URI); it is in WAL mode, so
  watch `opencode.db-wal` too when detecting changes.
- Skip rows without `tokens`; message ids are unique, so no de-duplication.
- Derive the provider from the model id when grouping by subscription.
