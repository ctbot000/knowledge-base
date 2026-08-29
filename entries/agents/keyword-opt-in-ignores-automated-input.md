---
title: A prompt keyword that unlocks an agent mode does not fire on scheduled input
tags: [agents, automation, scheduling]
added: 2026-08-29
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

## Fact

Agent harnesses that let a word in the prompt switch on an expensive mode gate
that trigger to human-typed input. The same word arriving from a scheduler, a
webhook payload, or a relayed comment is classified as non-human and the opt-in
is skipped — with no error and no log line. The mode has to be enabled through
configuration the run reads instead.

## Why it matters

An unattended job whose stored prompt contains the magic word looks correct and
keeps running in the default mode indefinitely. Nothing fails, so the gap is
usually noticed only when the output is compared against a manual run, and the
investigation starts from the wrong end: the prompt visibly contains the
trigger.

## How to apply

Enable the mode in a settings layer the run merges — a project- or task-scoped
settings file — and never by embedding the keyword in a stored prompt.

Confirm from the run's own record, not from the host UI. A host that does not
itself set the mode keeps showing its own last-picked value in the status chip
while the engine resolves something different from its settings, so the chip
and the run disagree. The run's transcript is where the applied value is
recorded.
