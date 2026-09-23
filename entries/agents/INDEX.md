# agents

- [An agent knowledge base is retrieval-limited, not storage-limited](knowledge-base-retrieval-limits.md) — What gets read back is the constraint, so the index line matters more than the entry body. `knowledge-base`, `context`, `retrieval`
- [A model's "supports tools" flag does not guarantee structured tool calls](tool-support-flag-is-not-a-guarantee.md) — Small models emit the call as plain text; the server reports no call and finish_reason "stop", and the agent silently stops. `llm`, `tool-calling`, `local-inference`
- [A prompt keyword that unlocks an agent mode does not fire on scheduled input](keyword-opt-in-ignores-automated-input.md) — Scheduler and webhook input classifies as non-human, so the opt-in is silently skipped; enable the mode in settings the run reads. `agents`, `automation`, `scheduling`
