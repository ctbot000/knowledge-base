# knowledge-base

Durable, general engineering knowledge, written to be read by an AI coding agent
and by a human.

Every entry here has to survive three changes of context: a different machine, a
different project, and six months. Anything that fails one of those tests belongs
somewhere else — see [CONVENTIONS.md](CONVENTIONS.md).

Browse it at **<https://ctbot000.github.io/knowledge-base/>** — searchable, one
page per entry. The site is generated from this Markdown and redeployed on every
push; nothing generated is committed.

## How it is used

An agent reads [INDEX.md](INDEX.md) at the start of a session: a table of
contents with one line per topic index. It opens the topic indexes that fit the
task — one line per entry, so scanning them is cheap — and then only the entries
whose summary is relevant to the task at hand.

When the agent learns something durable and general, it adds an entry, adds its
line to the topic index, and pushes.

## Layout

```
INDEX.md            table of contents — one line per topic index
CONVENTIONS.md      what belongs here, what does not, and how to write an entry
CLAUDE.md           operating instructions for an agent working in this repo
generate.py         builds the published site from the Markdown below
entries/
  <topic>/INDEX*.md one line per entry — the retrieval surface
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
