---
title: A search allowlist that rejects uncrawlable domains fails the whole query
tags: [search, web, agents]
added: 2026-08-22
---

## Fact

Web search APIs that accept a domain allowlist commonly validate it as a whole
rather than applying it as a filter. If any single domain in the list is one the
crawler cannot fetch, the request returns an error and yields zero results — the
other, perfectly good domains are not searched.

Anthropic's `WebSearch` behaves this way: one blocked domain in `allowed_domains`
returns a 400 naming the offenders, not a partial result set. Several major news
publishers block the crawler, so a hand-written "reputable sources" allowlist is
unusually likely to trip it.

## Why it matters

The intuition is that an allowlist narrows results, so adding one more domain can
only ever help. Here it is the opposite: each extra domain is another chance to
lose the entire query. An agent that builds a long allowlist of good sources gets
nothing back and may conclude, wrongly, that there is no news to report.

## How to apply

- Treat the allowlist as a set of required capabilities, not preferences. Keep it
  short, and only include domains already confirmed fetchable.
- Read the 400 — it names which domains were rejected. Drop exactly those and
  re-issue, rather than abandoning the allowlist and accepting unfiltered results.
- Maintain the known-good list per project instead of rediscovering it each run;
  which publishers block a given crawler changes slowly but does change.
- Never treat an errored search as an empty search. Zero results from a rejected
  query means "not asked", not "nothing found".
