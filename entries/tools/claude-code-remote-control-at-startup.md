---
title: Claude Code Remote Control can only be switched on from user-level settings
tags: [claude-code, settings, remote-control]
added: 2026-08-25
updated: 2026-08-26
sources:
  - https://docs.claude.com/en/docs/claude-code/settings
---

## Fact

`remoteControlAtStartup: true` starts the Remote Control bridge for every Claude
Code session. It is a security-sensitive setting, so it is only honored from
policy settings, `--settings` flag settings, and **user** settings. A project
`.claude/settings.json` or a local `.claude/settings.local.json` can set it to
`false` to opt a repository out, but setting it to `true` there does nothing.

This is the reverse of the usual precedence, where the more specific file wins.

## Why it matters

Putting the key in a project settings file looks correct and validates against
the schema, but the bridge never starts and there is no warning — the setting is
simply not read from that source. Time gets spent debugging the daemon instead of
the file it was written to.

The asymmetry is deliberate: a checked-in repository file must not be able to
expose a developer's sessions to a remote surface, but it must still be able to
withhold them.

## How to apply

Enable it once, globally, in the user settings file:

```json
{ "remoteControlAtStartup": true }
```

It takes effect on the next session; use the `/remote-control` command to attach
a session that is already running. To exempt a sensitive repository, add
`"remoteControlAtStartup": false` to that project's settings — a `false` from
project or local scope beats a `true` from user scope.

An administrator can remove the feature entirely with `disableRemoteControl` in
managed settings, which overrides all of the above.

## The setting arms a start, not a resume

`remoteControlAtStartup` is read when a session process starts fresh. A session
that is *resumed* into a new process comes back without the bridge, even with the
setting true — nothing re-arms it, and nothing says so.

This bites hardest after a desktop-app auto-update: the app quits, restarts, and
restores the open conversations. Sessions that were newly created afterwards get
the bridge automatically; the restored ones do not, so remote control silently
stops working for exactly the long-running session most likely to be relied on.

The omission is deliberate, not a gap. Auto-arming on resume was removed so that
resuming a conversation cannot silently take Remote Control away from another
session on the same machine that still holds it. Consequently there is no setting,
environment variable, or flag that restores it automatically: the launch-time
options that exist (`--remote-control`, `claude remote-control --continue`) apply
to starting a session from a terminal, not to one an app restores for you.

Re-attach with `/remote-control`, or the app's per-session toggle. It reconnects
to the same remote session rather than creating a second one, so any link already
shared stays valid. Where losing the conversation is acceptable, starting a new
session instead of resuming is the other way to get it back without a command. If remote control disappears without an obvious cause, check
whether the process was restarted before assuming a network or auth problem —
an expired OAuth token is a different failure and does not drop an already
connected bridge.
