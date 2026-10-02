# Index

One line per topic index. Scan this first, open the topic indexes that fit the
task — one line per entry, with the entry files beside them — and then only the
entries that are relevant.

Adding an entry? Read [CONVENTIONS.md](CONVENTIONS.md) — the generality bar is
strict and this repository is public.

- [agents](entries/agents/INDEX.md) — Working with LLM coding agents: knowledge-base retrieval, unreliable tool-call support, mode keywords that scheduled input does not trigger.
- [languages](entries/languages/INDEX.md) — Language semantics that bite: JavaScript `-0` and `NaN`, invisible line terminators (U+2028), Python asyncio shutdown, Java name shadowing, GLSL reserved words.
- practices — indexed by subject:
  - [web front end](entries/practices/INDEX-web.md) — CSS layout and cascade (flex, grid, container units, 3D transforms, media-query breakpoints), text wrapping and truncation (Korean line breaks, emoji pairs, line clamping, ellipsis checks), DOM events and pointer gestures, rAF and hidden-page throttling, Canvas 2D, SVG, Web Audio, Web Speech, getUserMedia, EventSource, localStorage, ARIA, UI state and dialogs, full screen and installed-app detection.
  - [graphics and geometry](entries/practices/INDEX-graphics.md) — 3D scenes and cameras, lighting, colour and shaders, mesh winding and culling, terrain and procedural geometry, level of detail, image processing and computer vision (QR detection, perspective from reference points), diagram label placement, direction markers on maps.
  - [simulation and game design](entries/practices/INDEX-simulation.md) — Physics and contact solvers, control loops, game balance and difficulty, simulated players and bots, procedural levels and puzzles, cooldowns and game-loop timing.
  - [general](entries/practices/INDEX.md) — CLI input, shell quoting and signals, sockets and chunked text framing (surrogate pairs), HTTP servers and path-traversal testing, upgrades and streamed responses, refresh-token auth, cron, git, Android, generated files, and testing or debugging habits that apply anywhere.
- systems — No entries yet: databases, networking, performance, distributed behavior. Socket and HTTP facts so far are under practices: general.
- [tools](entries/tools/INDEX.md) — GitHub, Actions and Pages (Jekyll, kramdown); Markdown rendering (math, bold next to Korean/Japanese/Chinese text); Claude Code and Claude Desktop; browser automation and headless testing (screenshots, synthetic input, hit tests, paint order and box-overlap checks, state that lags a resize or layout change, touch or mouse mode, fake camera and microphone streams, hidden tabs, Puppeteer, software rendering and reproducing CI speed); game-loop test harnesses; node (its test runner, its navigator global), npm, javac, Gradle; curl uploads, unzip and ZIP files; yt-dlp, ffmpeg and Homebrew; three.js, Tk, Chrome extensions, PeerJS signaling and message limits; dev servers, caching and vendored ESM.
