# knowledge-base

Durable, general engineering knowledge, written to be read by an AI coding agent
and by a human.

Every entry here has to survive three changes of context: a different machine, a
different project, and six months. Anything that fails one of those tests belongs
somewhere else — see [CONVENTIONS.md](CONVENTIONS.md).

## How it is used

An agent reads [INDEX.md](INDEX.md) at the start of a session. The index is one
line per entry, so scanning it is cheap. The agent then opens only the entries
whose summary is relevant to the task at hand.

When the agent learns something durable and general, it adds an entry, updates
the index, and pushes.

## Layout

```
INDEX.md            one line per entry — the retrieval surface
CONVENTIONS.md      what belongs here, what does not, and how to write an entry
CLAUDE.md           operating instructions for an agent working in this repo
entries/
  languages/        language-level behavior, semantics, idioms
  tools/            build tools, version control, CLIs, editors
  practices/        testing, review, design, process
  systems/          databases, networking, performance, distributed behavior
  agents/           working with LLM coding agents: prompts, skills, harnesses
```

## What this is not

Not a notebook, not a changelog, and not a mirror of official documentation. If a
single web search answers it just as well, it does not need an entry. The value
is in the things that were expensive to learn the first time.
