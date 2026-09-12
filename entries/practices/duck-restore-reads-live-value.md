---
title: A duck-and-restore that reads its restore level from the live node latches the ducked value
tags: [web-audio, state, audio]
added: 2026-09-12
---

## Fact

The usual way to silence something briefly is to save what it is set to, force it
to zero, and schedule it back:

```js
const target = gain.gain.value;        // <- the bug
gain.gain.cancelScheduledValues(t);
gain.gain.setValueAtTime(0, t);
gain.gain.setValueAtTime(target, t + 0.15);
```

Run it twice inside that window and the second call reads the *ducked* value as
the thing to restore, while `cancelScheduledValues` discards the restore the
first call had scheduled. The node is now pinned at zero with nothing left to
undo it.

Overlapping calls are the normal case rather than an edge case, because one such
helper is usually wired to several events that fire together — pause, quit,
navigate away, lose focus.

## Why it matters

Nothing throws and nothing looks wrong. The graph is intact, sources still start
and stop on time, and every check upstream of the node reads correct values.
Only the output is gone, and it stays gone for the rest of the session.

The symptom also surfaces long after the two calls that caused it, so it reads as
"the synth stopped working" and sends the search into voice allocation and
scheduling rather than into a mute helper that ran twice.

## How to apply

- Restore from a constant the code owns, never from the node's current value. The
  design-time level is a fact about the design, not about the node.
- The same shape bites any save/restore pair whose trigger can re-enter: a
  stashed scroll position, a saved `disabled` flag, a cursor swapped for the
  duration of a drag. If the save can run while the temporary value is in place,
  it must not read it.
- Where re-entrancy is expected by design, prefer a depth counter or a single
  owner over save/restore.
