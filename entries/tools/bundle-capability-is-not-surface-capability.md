---
title: A capability found in an app bundle belongs to some surface, not necessarily the one in front of you
tags: [debugging, desktop-apps, markdown]
added: 2026-09-06
---

## Fact

A desktop app ships several renderers. Grepping its bundle proves a library is
present somewhere in the product; it says nothing about which pane loads it. A
chat window, a code pane, a settings view and an embedded webview can each run a
different Markdown pipeline out of the same install directory.

Concretely: an Electron app can carry `rehype-katex` plus a full KaTeX engine in
its web assets, configured with `singleDollarTextMath: false` — while a second
surface in the same app renders through a terminal-flavoured pipeline with no
math support at all. Finding the first and concluding the second will typeset
`$$…$$` is a mis-attribution, not a discovery.

## Why it matters

Bundle evidence feels stronger than it is, because it is concrete: a real config
value, in a real shipping file. It reads as a finding rather than a guess, so it
gets reported with unearned confidence — and the user is the one who has to
disprove it.

## How to apply

**Rank the evidence.** What a human reports seeing on the screen outranks what a
grep found. When they disagree, the grep hit is about a different surface.

**Attribute before concluding.** Which bundle, loaded by which window? An asset
directory whose name matches neither the pane nor the process you are inspecting
is a warning, not a detail.

**Bundle evidence is a hypothesis; a rendered result is the test.** State it as
one — "the bundle suggests X; confirm by trying it" — and let the round trip
settle it, rather than announcing the fix and being corrected.

**Prefer a surface you control.** When the display surface cannot be changed,
move the content to one whose renderer you author (a published page, a file
whose viewer you know) instead of negotiating with an opaque one.
