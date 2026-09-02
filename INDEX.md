# Index

One line per entry. Scan this first; open only what is relevant.

Adding an entry? Read [CONVENTIONS.md](CONVENTIONS.md) — the generality bar is
strict and this repository is public.

## agents

- [An agent knowledge base is retrieval-limited, not storage-limited](entries/agents/knowledge-base-retrieval-limits.md) — What gets read back is the constraint, so the index line matters more than the entry body. `knowledge-base`, `context`, `retrieval`
- [A model's "supports tools" flag does not guarantee structured tool calls](entries/agents/tool-support-flag-is-not-a-guarantee.md) — Small models emit the call as plain text; the server reports no call and finish_reason "stop", and the agent silently stops. `llm`, `tool-calling`, `local-inference`
- [A prompt keyword that unlocks an agent mode does not fire on scheduled input](entries/agents/keyword-opt-in-ignores-automated-input.md) — Scheduler and webhook input classifies as non-human, so the opt-in is silently skipped; enable the mode in settings the run reads. `agents`, `automation`, `scheduling`

## languages

- [asyncio's Server.wait_closed() waits for live connections, not just the listener](entries/languages/asyncio-wait-closed-waits-for-connections.md) — Since Python 3.12 it blocks until every handler ends, so awaiting it before telling clients to leave deadlocks. `python`, `asyncio`, `shutdown`

## practices

- [Cron cannot express an every-N-hours interval unless N divides 24](entries/practices/cron-interval-must-divide-period.md) — `*/5` on hours wraps to a 4-hour gap at midnight; use an interval timer or a self-rescheduling one-shot instead. `cron`, `scheduling`, `automation`
- [A CLI that reads piped stdin hangs when its parent leaves the pipe open](entries/practices/cli-stdin-read-hangs.md) — `isatty` says "not a terminal", not "has data"; a pipe with no writer never reaches EOF. `cli`, `stdin`, `subprocess`
- [An interactive REPL needs one long-lived input reader, not one per prompt](entries/practices/repl-single-input-reader.md) — A reader opened per prompt drops type-ahead and every line of a paste after the first. `cli`, `repl`, `terminal`
- [An HTTP upgrade hands over bytes already read past the handshake](entries/practices/http-upgrade-head-buffer.md) — The `head` buffer holds the new protocol's first frames; ignore it and a server's greeting vanishes on loopback. `http`, `websocket`, `protocols`
- [An author display rule silently overrides the HTML hidden attribute](entries/practices/hidden-attribute-vs-display-rule.md) — `[hidden]` is only a UA stylesheet rule, so any class setting `display` keeps the element painted while `el.hidden` reads true. `css`, `html`, `dom`
- [One key press runs two steps when a bubbling handler reads state an inner handler just changed](entries/practices/key-event-runs-two-steps.md) — Dispatch is synchronous, so a delegated handler sees the flag the inner one just flipped; `stopPropagation` is the fix. `dom`, `events`, `keyboard`
- [An animation lifetime counted in frames never expires while rAF is throttled](entries/practices/animation-lifetime-in-frames.md) — A hidden tab stops delivering frames, so a `life--` counter stalls and the overlay freezes on screen; end effects on wall-clock time. `animation`, `browser`, `requestAnimationFrame`
- [A swallowed storage write needs an in-memory copy, or the next read contradicts it](entries/practices/swallowed-storage-write-stale-read.md) — `try/catch` around `localStorage` hides the failure, not the consequence; re-reading the key returns the old value and the session contradicts itself. `storage`, `caching`, `error-handling`
- [A bare text node in a flex container becomes its own flex item](entries/practices/flex-container-wraps-bare-text-nodes.md) — It is wrapped in an anonymous flex item, so a label and its unit span land on separate rows and every item count is off by one. `css`, `flexbox`, `layout`
- [An inline SVG sizes itself from its viewBox unless both axes are definite](entries/practices/svg-intrinsic-size-beats-the-box.md) — A `viewBox` ratio blows up `1fr` grid tracks and beats `position:absolute` insets, so the graphic overflows and the next row paints over it. `css`, `svg`, `layout`
- [A no-guess puzzle board is found by rejection sampling against a solver that only makes the player's deductions](entries/practices/no-guess-puzzle-generation.md) — Keep a random board only if a deliberately weak solver clears it; cheap enough to run at first click, but acceptance collapses as density rises. `algorithms`, `puzzles`, `game-design`
- [Electron's findInPage findNext option starts a search session, it does not step to the next match](entries/practices/findinpage-findnext-starts-a-session.md) — `findNext: false` on the first request is dropped silently and `found-in-page` never fires; omitting the option starts a session. `electron`, `browser`, `find-in-page`
- [A shrinkable flex item contributes its content width, not its flex-basis, to an auto-sized container](entries/practices/flex-basis-does-not-size-an-auto-container.md) — `flex: 0 1 190px` renders at the text's width; use `width` for a fixed preferred size. `css`, `flexbox`, `layout`
- [Closing a socket with unread data sends RST, which can destroy what you just wrote](entries/practices/close-with-unread-data-sends-rst.md) — The peer sees ECONNRESET instead of the error you wrote; half-close and drain before closing. `tcp`, `sockets`, `networking`
- [One ACTIVITY_PAUSED does not mean the app left the foreground](entries/practices/activity-paused-is-not-app-backgrounded.md) — Usage events report activities, not apps; closing the session on the first pause silently under-counts foreground time. `android`, `usage-stats`, `instrumentation`
- [checkSelfPermission(POST_NOTIFICATIONS) answers DENIED on Android below 13](entries/practices/post-notifications-denied-below-api-33.md) — The permission does not exist pre-33, so the obvious guard mutes every notification on Android 10-12. `android`, `permissions`, `notifications`

## systems

_No entries yet._

## tools

- [Android Gradle Plugin 9 applies Kotlin itself and fails if you also apply the Kotlin plugin](entries/tools/agp9-applies-kotlin-itself.md) — The standalone `kotlin.android` plugin is now a hard build failure, and `android.kotlinOptions` is gone with it. `android`, `gradle`, `kotlin`
- [gh repo create does not add a git remote unless you pass --source](entries/tools/gh-repo-create-no-remote.md) — The push then fails with a misleading "access rights" error; check `git remote -v` first. `git`, `github`, `cli`
- [Enabling GitHub Pages from the CLI is an API POST, and its success does not mean the site is live](entries/tools/gh-enable-pages-is-an-api-post.md) — `gh` has no `pages` command; the nested `source` needs bracketed `-f` keys, and the returned URL is live only once `.status` reaches `built`. `github`, `github-pages`, `cli`
- [A search allowlist that rejects uncrawlable domains fails the whole query](entries/tools/allowed-domains-all-or-nothing.md) — One blocked domain returns 400 and zero results; an errored search is not an empty search. `search`, `web`, `agents`
- [Most `"type": "user"` lines in a Claude Code transcript were not typed by the user](entries/tools/claude-code-transcript-human-prompts.md) — Tool results share the `user` role; filter on `origin.kind == "human"` or overcount prompts ~20x. `claude-code`, `transcripts`, `jsonl`
- [A Claude Code session's subagent transcripts live beside the session file, not inside it](entries/tools/claude-code-subagent-transcripts-are-separate-files.md) — Subagent turns go to `<session-id>/subagents/**/agent-*.jsonl`; parsing only the session file silently drops most of the run. `claude-code`, `transcripts`, `jsonl`
- [Claude Desktop restarts itself to install updates, and only an MDM policy stops it](entries/tools/claude-desktop-stealth-update-restart.md) — An idle timer quits the app; restored sessions lose Remote Control and can fall back to the previous Claude Code build. `disableAutoUpdates` in managed preferences is the sole off switch. `claude-code`, `claude-desktop`, `updates`
- [Claude Code Remote Control can only be switched on from user-level settings](entries/tools/claude-code-remote-control-at-startup.md) — `remoteControlAtStartup` is read from policy/flag/user scope only, and arms a fresh start but not a resume — an app auto-update drops it. `claude-code`, `settings`, `remote-control`
- [yt-dlp re-encodes a file it already produced unless final_ext names the output](entries/tools/yt-dlp-final-ext-enables-skip.md) — The existing-file check maps the download name to the finished one through `final_ext`; without it every run re-downloads and re-encodes, silently. `yt-dlp`, `media`, `python`
- [yt-dlp's ffmpeg_location does not reach its own partial-download check](entries/tools/yt-dlp-ffmpeg-location-misses-path-checks.md) — Section downloads probe `PATH` only and abort with "ffmpeg is not installed" despite a correct flag; put the directory on `PATH`. `yt-dlp`, `media`, `ffmpeg`
- [element.focus() moves activeElement but fires no focus event while the view lacks system focus](entries/tools/focus-events-defer-in-an-unfocused-view.md) — The field accepts text while the focus handler never ran, so automation passes against state the app never set. `testing`, `automation`, `focus`
- [A screenshot can show a frame older than the DOM state you just set](entries/tools/screenshot-lags-committed-dom-state.md) — Hidden and backgrounded surfaces may not paint, so the image shows the pre-change style; assert against getComputedStyle instead. `testing`, `automation`, `browser`
- [Synthetic key events do not trigger the native activation a real key press does](entries/tools/synthetic-key-events-not-real-presses.md) — Untrusted events run no default action and injected ones may arrive with an empty `e.key`; check `isTrusted` before blaming the app. `testing`, `automation`, `keyboard`
