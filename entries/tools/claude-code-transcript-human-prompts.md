---
title: Most `"type": "user"` lines in a Claude Code transcript were not typed by the user
tags: [claude-code, transcripts, jsonl]
added: 2026-08-26
---

## Fact

Claude Code appends every session to a JSONL transcript under
`~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`. In those files the role
`user` covers everything fed back into the model, not just human input: tool
results, hook output, attachments, and system reminders are all `"type":
"user"`. On Claude Code 2.1.x, real human input is the subset carrying
`"origin": {"kind": "human"}`; tool results have no `origin` at all.

The proportion is lopsided. Across one machine's full history — 67 sessions,
about 3,200 `user` lines — 168 were actually typed by a person, a little over
5%.

## Why it matters

Anything that mines a prompt history — usage analysis, recovering what was asked,
building a corpus of a user's own writing — gets a ~20x overcount and a corpus
dominated by `git status` output if it filters on role alone. The error is silent:
the extraction succeeds and returns plausible-looking text.

## How to apply

Filter positively on the origin marker rather than trying to exclude tool results:

```python
d.get("type") == "user"
and (d.get("origin") or {}).get("kind") == "human"
and not d.get("isSidechain") and not d.get("isMeta")
```

Then still strip, from the surviving text:

- `<system-reminder>…</system-reminder>`, injected into otherwise human turns
- `<command-name>` / `<command-args>` / `<local-command-stdout>` blocks — slash
  commands, some of which carry no `origin` field either
- `<scheduled-task>…</scheduled-task>` — an automated run's prompt, authored
  earlier and replayed, not typed at that moment
- `isSidechain: true` lines, which are a subagent's conversation, not the user's

Deduplicate afterwards: resumed sessions replay earlier turns, and `queue-operation`
lines repeat a prompt's text a second time. Confirm the marker on the versions you
actually have — it is a format detail, not a documented API, so verify rather than
assume it holds for older or newer builds.
