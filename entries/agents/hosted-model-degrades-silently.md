---
title: A hosted model can degrade silently, with every call still succeeding
tags: [llm, agents, monitoring, json-mode]
added: 2026-11-28
---

## Fact

A hosted model's answers can turn malformed for hours with no error to show for
it: the same model name, prompt and code, HTTP 200 and finish reason "stop",
while the share of answers that fail to parse or carry garbled keys jumps from a
few percent to most of them. In JSON mode it shows as mangled keys (`"thought"`
run on into nonsense words, a required key missing) and as JSON that does not
parse: `json_object` mode asks for JSON; it does not enforce a schema, and on
some providers not even valid syntax.

## Why it matters

An agent loop treats each bad answer as one wasted step and asks again, so a
degraded provider looks like a model that dithers: it burns its step budget, is
nudged to act, hands off unfinished work, and the run gets blamed on the task or
the prompt. Error-rate monitoring sees nothing, because nothing failed. A few
5xx errors from the same provider in the same window are a hint; the bad answers
themselves arrive as successes.

## How to apply

- Count malformed answers per run (unparsable, unknown keys, a required field
  missing) and keep the rate beside tokens and steps. A run far above the usual
  rate, with no code change, points at the provider, not the task.
- When the rate jumps, pause the agents and try later instead of letting runs
  spend their step budgets on retries.
- Where the provider offers schema-constrained decoding (strict structured
  outputs or native tool calls), prefer it to a schema pasted into the prompt
  plus JSON mode: it rules out mangled keys, though not a poor answer.
