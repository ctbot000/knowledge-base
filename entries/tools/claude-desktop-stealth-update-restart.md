---
title: Claude Desktop restarts itself to install updates, with no opt-in and no setting
tags: [claude-code, claude-desktop, updates]
added: 2026-08-26
updated: 2026-08-26
---

## Fact

The Claude desktop app updates itself by default. Nothing has to be enabled: on
launch it logs `[updater] App is installed, enabling initial check and
auto-updates`, downloads any new build in the background, then waits for the app
to go idle and quits to install it — `[stealth-update] Triggering stealth update
after idle timeout`, followed by `beforeQuitForUpdate`. There is no user-facing
toggle; the app's `config.json` stores only what version was last seen, not a
preference.

The behavior is **server-gated, not tied to an app version**. The same installed
build can hold a downloaded update indefinitely until the user installs it, and
then, days later with no version change in between, start installing on its own.
Once it is on, the gap between "update downloaded" and the self-restart is about
ten minutes of idle time; before it, staged updates sit for hours, logging
`Staged version X is still current` every 20 minutes and waiting.

The app and the Claude Code it bundles are on **separate version tracks** and
update independently. An app restart therefore does not imply the CLI version
changed, or vice versa.

## Why it matters

A long-running session can be restarted underneath you without any prompt, at a
moment chosen by an idle timer rather than by you. Two consequences that look
like unrelated bugs:

- Remote Control silently stops working. `remoteControlAtStartup` arms a fresh
  start, not the resume that follows the restart, so the restored session comes
  back with no bridge while sessions created afterwards get one normally.
- The restored session can run the **older** Claude Code build. The new bundle is
  still downloading when sessions are restored, so they log `[CCD] Falling back
  to installed version: <previous>`. Sessions started a few minutes later get the
  new one, leaving two versions running side by side on the same machine.

## How to apply

- Do not assume today's behavior is what the app will do tomorrow, and do not
  expect an app update to be what changed it. Compare `beforeQuitForUpdate` lines
  in the log: a `[stealth-update] Triggering stealth update after idle timeout`
  immediately above one means the app chose the moment; its absence means a person
  did.
- Do not read an unexplained session restart as a crash. Check the log for
  `stealth-update` / `beforeQuitForUpdate` before investigating further; the log
  lives at `~/Library/Logs/Claude/main.log` on macOS.
- After any such restart, re-attach Remote Control with `/remote-control` — it
  reconnects to the same remote session, so an already-shared link stays valid.
- If a session behaves like an older build, compare its version against a
  freshly started one rather than assuming both are current. Restarting the
  session picks up the downloaded build and re-arms Remote Control at the same
  time.
