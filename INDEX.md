# Index

One line per entry. Scan this first; open only what is relevant.

Adding an entry? Read [CONVENTIONS.md](CONVENTIONS.md) — the generality bar is
strict and this repository is public.

## agents

- [An agent knowledge base is retrieval-limited, not storage-limited](entries/agents/knowledge-base-retrieval-limits.md) — What gets read back is the constraint, so the index line matters more than the entry body. `knowledge-base`, `context`, `retrieval`
- [A model's "supports tools" flag does not guarantee structured tool calls](entries/agents/tool-support-flag-is-not-a-guarantee.md) — Small models emit the call as plain text; the server reports no call and finish_reason "stop", and the agent silently stops. `llm`, `tool-calling`, `local-inference`

## languages

_No entries yet._

## practices

- [Cron cannot express an every-N-hours interval unless N divides 24](entries/practices/cron-interval-must-divide-period.md) — `*/5` on hours wraps to a 4-hour gap at midnight; use an interval timer or a self-rescheduling one-shot instead. `cron`, `scheduling`, `automation`
- [A CLI that reads piped stdin hangs when its parent leaves the pipe open](entries/practices/cli-stdin-read-hangs.md) — `isatty` says "not a terminal", not "has data"; a pipe with no writer never reaches EOF. `cli`, `stdin`, `subprocess`
- [An interactive REPL needs one long-lived input reader, not one per prompt](entries/practices/repl-single-input-reader.md) — A reader opened per prompt drops type-ahead and every line of a paste after the first. `cli`, `repl`, `terminal`

## systems

_No entries yet._

## tools

- [gh repo create does not add a git remote unless you pass --source](entries/tools/gh-repo-create-no-remote.md) — The push then fails with a misleading "access rights" error; check `git remote -v` first. `git`, `github`, `cli`
- [A search allowlist that rejects uncrawlable domains fails the whole query](entries/tools/allowed-domains-all-or-nothing.md) — One blocked domain returns 400 and zero results; an errored search is not an empty search. `search`, `web`, `agents`
- [Most `"type": "user"` lines in a Claude Code transcript were not typed by the user](entries/tools/claude-code-transcript-human-prompts.md) — Tool results share the `user` role; filter on `origin.kind == "human"` or overcount prompts ~20x. `claude-code`, `transcripts`, `jsonl`
- [Claude Desktop restarts itself to install updates, with no opt-in and no setting](entries/tools/claude-desktop-stealth-update-restart.md) — An idle timer quits the app; restored sessions lose Remote Control and can fall back to the previous Claude Code build. `claude-code`, `claude-desktop`, `updates`
- [Claude Code Remote Control can only be switched on from user-level settings](entries/tools/claude-code-remote-control-at-startup.md) — `remoteControlAtStartup` is read from policy/flag/user scope only, and arms a fresh start but not a resume — an app auto-update drops it. `claude-code`, `settings`, `remote-control`
