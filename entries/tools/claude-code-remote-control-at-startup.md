---
title: Claude Code Remote Control can only be switched on from user-level settings
tags: [claude-code, settings, remote-control]
added: 2026-08-25
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
