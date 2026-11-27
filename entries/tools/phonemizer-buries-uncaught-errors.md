---
title: Importing phonemizer in Node buries every uncaught error under its megabyte-long minified source
tags: [node, phonemizer, kokoro, emscripten, text-to-speech, debugging]
added: 2026-11-27
sources:
  - https://github.com/xenova/phonemizer.js
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

The error is still printed, but last, after more than a megabyte of noise, so
anything that shows the head of the output, a log viewer or a tool result that
truncates, shows only the library's source. A crash in the app's own code
looks like a crash inside the speech library.

## How to apply

- Register your own handlers before the first import of `kokoro-js` or
  `phonemizer` (handlers run in the order added) that print the stack and call
  `process.exit(1)`.
- To read a log that already has it, take the tail, not the head.
- In a library built with Emscripten, `-sNODEJS_CATCH_EXIT=0
  -sNODEJS_CATCH_REJECTION=0` keeps it from touching the host's handlers.
