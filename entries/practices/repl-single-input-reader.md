---
title: An interactive REPL needs one long-lived input reader, not one per prompt
tags: [cli, repl, terminal, ux]
added: 2026-08-21
---

## Fact

Opening a fresh line reader for each prompt and closing it after the answer
silently discards anything typed while no reader was open. Input does not wait
politely between prompts: keystrokes that arrive while the program is busy, and
every line after the first in a paste, land in a window where nothing is
listening.

The fix is structural, not a tuning parameter. One reader is created at startup
and lives for the whole session, pushing every completed line onto a queue. A
prompt takes the next queued line if one is waiting and otherwise blocks on the
queue.

## Why it matters

This is exactly the input a user most wants preserved: the follow-up they typed
while a long operation ran, and the second through last lines of a paste. Losing
it reads as the program eating keystrokes, and it is invisible in manual testing
because a human naturally waits for the prompt before typing.

The same gap swallows input during any phase that grabs the terminal directly —
a raw-mode key handler installed to catch Ctrl+C during a long turn will consume
and drop every other keystroke unless it feeds the same queue.

## How to apply

- Create the reader once; expose `readLine()` as "shift the queue, else await".
- Route interrupt handling through the same reader (its own signal/keypress
  events) rather than attaching a second competing listener to the input stream.
- Accept that keystrokes echo during long operations. That is the visible cost of
  keeping the reader live, and showing type-ahead is better than dropping it.
- Test with timed input, not an instant pipe: input delivered before startup
  finishes, followed immediately by EOF, exercises a different path and will fail
  for unrelated reasons.
