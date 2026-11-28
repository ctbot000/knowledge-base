---
title: Importing phonemizer in Node buries every uncaught error under its megabyte-long minified source
tags: [node, phonemizer, kokoro, emscripten, text-to-speech, debugging]
added: 2026-11-27
updated: 2026-11-28
sources:
  - https://github.com/xenova/phonemizer.js
  - https://github.com/xenova/phonemizer.js/pull/7
  - https://emscripten.org/docs/tools_reference/settings_reference.html#nodejs-catch-exit
---

## Fact

The `phonemizer` npm package (espeak-ng built with Emscripten; it is what
`kokoro-js` phonemizes with) installs process-wide `uncaughtException` and
`unhandledRejection` handlers that throw the error again. Node then reports any
uncaught error in the whole process as thrown from `phonemizer.js:1`: it prints
that line, about 1.3 MB of minified code with data inside it, a caret line, and
only then the real message, and exits with code 7 instead of 1. Seen with
phonemizer 1.2.1 on Node 26.

## Why it matters

The message comes last, after more than a megabyte of noise, so a log viewer or
a tool result that keeps the head shows only the library's source; through a
pipe on macOS it never arrives at all ([a dying process's piped output stops at
64 KiB](node-piped-output-cut-at-64kib-on-exit-macos.md)). A crash in the app's
own code looks like one inside the speech library, and the app's own
`uncaughtException` handler cannot keep the process running: the library's
handler throws anyway.

## How to apply

- Register your own handlers before the first import of `kokoro-js` or
  `phonemizer` (handlers run in the order added) that print the stack and call
  `process.exit(1)`.
- To read a log that already has it, write stderr to a file and take the tail.
- In a library built with Emscripten, `-sNODEJS_CATCH_EXIT=0
  -sNODEJS_CATCH_REJECTION=0` keeps it from touching the host's handlers; a
  change removing them from phonemizer is proposed upstream (PR #7).
