---
title: A Claude Code session's subagent transcripts live beside the session file, not inside it
tags: [claude-code, transcripts, jsonl]
added: 2026-08-29
---

## Fact

Claude Code writes a session to `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`,
but a subagent's or workflow agent's own conversation is not appended to that
file. It goes into a sibling directory named after the session:

```
<encoded-cwd>/<session-id>/subagents/<kind>/<group>/agent-<agentId>.jsonl
<encoded-cwd>/<session-id>/subagents/<kind>/<group>/agent-<agentId>.meta.json
<encoded-cwd>/<session-id>/subagents/<kind>/<group>/journal.jsonl
```

The agent file holds that agent's full turn stream — prompt, thinking, tool
calls, results — with `isSidechain: true` and its `agentId` on every record.
`journal.jsonl` holds the `started` / `result` lifecycle records. The session
file itself keeps only the tool call that spawned the run and whatever summary
came back; on a store where every subagent ran this way it contains **zero**
`isSidechain` lines and never mentions an `agentId`.

## Why it matters

Anything that reads a session — a transcript viewer, a token accounting script,
an audit of what an agent actually did — silently under-reports when it parses
`<session-id>.jsonl` alone. The parent looks like a short session that made one
tool call, while most of the model's output for that turn sits in files the
reader never opened. Nothing errors; the numbers are just wrong.

## How to apply

Treat the session directory, not the session file, as the unit:

```python
main   = store / project / f"{session_id}.jsonl"
agents = sorted((store / project / session_id).rglob("*.jsonl"))
```

To join a subagent back to the parent turn that spawned it, use `promptId` —
the parent's tool call and the subagent's first message share it. Do not rely
on the parent referencing `agentId`; it generally does not. Older runs may
instead inline sidechain records in the session file, so handle both. See
[[claude-code-transcript-human-prompts]] for the other trap in the same files.
