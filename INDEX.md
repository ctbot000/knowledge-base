# Index

One line per entry. Scan this first; open only what is relevant.

Adding an entry? Read [CONVENTIONS.md](CONVENTIONS.md) — the generality bar is
strict and this repository is public.

## agents

- [An agent knowledge base is retrieval-limited, not storage-limited](entries/agents/knowledge-base-retrieval-limits.md) — What gets read back is the constraint, so the index line matters more than the entry body. `knowledge-base`, `context`, `retrieval`

## languages

_No entries yet._

## practices

- [Cron cannot express an every-N-hours interval unless N divides 24](entries/practices/cron-interval-must-divide-period.md) — `*/5` on hours wraps to a 4-hour gap at midnight; use a self-rescheduling one-shot for true intervals. `cron`, `scheduling`, `automation`
- [A CLI that reads piped stdin hangs when its parent leaves the pipe open](entries/practices/cli-stdin-read-hangs.md) — `isatty` says "not a terminal", not "has data"; a pipe with no writer never reaches EOF. `cli`, `stdin`, `subprocess`
- [An interactive REPL needs one long-lived input reader, not one per prompt](entries/practices/repl-single-input-reader.md) — A reader opened per prompt drops type-ahead and every line of a paste after the first. `cli`, `repl`, `terminal`

## systems

_No entries yet._

## tools

_No entries yet._
