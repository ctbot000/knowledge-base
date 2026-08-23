---
title: A model's "supports tools" flag does not guarantee structured tool calls
tags: [llm, tool-calling, agents, local-inference]
added: 2026-08-23
---

## Fact

Model registries and serving stacks advertise tool support as a boolean
capability. It means the model was trained on tool-use data and its chat
template has slots for calls — not that any given response will fill them.

Smaller instruct models regularly emit the call as ordinary assistant text:

```json
{"name": "read", "arguments": {"file_path": "src/stats.js"}}
```

The server sees no call in the format its parser expects, so the API returns
that string as message content, an empty tool-call field, and a finish reason of
"stop". Nothing errors. The agent sees a normal final answer and stops.

## Why it matters

The failure is silent and reads as a model that "ignored the tools", so it gets
misdiagnosed as a prompt problem or a missing capability. The real cause is a
template mismatch between what the model generated and what the server parses,
and it is invisible in any test that mocks the server — the mock returns
whatever well-formed shape the test author wrote.

It is also the difference between an agent that works against self-hosted models
and one that does not. Below roughly 7B parameters this is common enough to be
the default experience.

## How to apply

- Treat a missing tool call plus content that parses as a tool-call object as a
  recoverable case. Extract calls whose name matches a tool actually declared in
  the request, and ignore everything else so ordinary prose containing JSON is
  not misread.
- Scan for balanced brace spans rather than assuming the whole message is JSON —
  models wrap calls in prose, code fences, or `<tool_call>` tags.
- **Refuse malformed JSON instead of repairing it.** A half-parsed call carries
  arguments that write files or run commands; failing loudly is correct.
- Do not stream such text to the user before the turn ends. Withhold content
  that opens with `{` or a call wrapper, then release it as prose only if
  recovery does not claim it.
- Verify against a real server before believing tool use works. A mocked
  backend only ever returns the shape you wrote into the mock.
