---
title: An agent knowledge base is retrieval-limited, not storage-limited
tags: [knowledge-base, context, retrieval, documentation]
added: 2026-08-19
---

## Fact

A knowledge base read by an LLM agent is constrained by what gets pulled back
into context, not by what was written down. Storage is free and unbounded;
context is neither. An entry that is never retrieved has the same value as an
entry that was never written, and it costs more, because it dilutes whatever
index the agent scans to decide what to read.

## Why it matters

The intuitive failure mode is writing too little. The actual failure mode is
writing too much: every marginal entry lengthens the index, and a long index is
either skimmed carelessly or skipped entirely. Past that point, adding knowledge
makes the knowledge base worse — a base of 500 entries where 30 are worth reading
performs strictly worse than one holding only those 30.

This also means the retrieval surface is a different artifact from the content.
A one-line summary written as a description of the entry ("notes on caching")
is useless for the only decision it is ever used for: open this file or not.

## How to apply

- **Write the index line for the open/skip decision.** It should state the claim,
  not the topic. `Prepared statements are cached per connection, not per pool`
  earns an open; `notes on prepared statements` does not.
- **Treat the index as the scarce resource.** Cap it at one line per entry, and
  when it outgrows a single scan, split it into per-topic indexes rather than
  letting it sprawl.
- **Make entries self-contained.** An agent typically opens one file, not the
  graph around it. Cross-links are for humans and for follow-up; the entry has to
  stand alone.
- **Delete aggressively.** Removing a stale or low-value entry is a direct
  improvement to retrieval, not a loss of information. Apply the same standard to
  entries that turned out to be wrong: rewrite or delete, never annotate.
- **Resist padding.** The instinct to seed a new knowledge base with general
  facts already known to the model is exactly the failure this describes.
